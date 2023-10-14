import dataclasses
import datetime
import enum
import re
import typing

import fsspec
import pystac
import xarray as xr
import xstac


class Product(str, enum.Enum):
    CHANNEL_RT = "channel_rt"
    LAND = "land"
    RESERVOIR = "reservoir"
    TERRAIN_RT = "terrain_rt"


class Region(str, enum.Enum):
    CONUS = "conus"


class Category(str, enum.Enum):
    SHORT_RANGE = "short_range"


@dataclasses.dataclass
class NWMInfo:
    """
    Examples
    --------
    >>> info = NWMInfo.from_filename(
    ...     "nwm.20231010/short_range/nwm.t00z.short_range.channel_rt.f001.conus.nc"
    ... )
    >>> info
    """

    date: datetime.datetime
    category: Category  # literal / enum
    cycle_runtime: int  # literal / enum
    product: Product
    forecast_hour: int
    region: Region

    pattern = re.compile(
        "nwm\.(?P<date>\d{8})/"
        "(?P<category>short_range)"
        "/nwm\.t(?P<cycle_runtime>"
        "\d{2})z\.short_range\."
        "(?P<product>(channel_rt|land|reservoir|terrain_rt))\."
        "f(?P<forecast_hour>\d{3})\."
        "(?P<region>conus)\.nc"
    )

    @classmethod
    def from_filename(cls, s: str) -> "NWMInfo":
        m = cls.pattern.match(s)
        assert m
        d = m.groupdict()

        date = datetime.datetime.strptime(d["date"], "%Y%m%d")
        category = Category(d["category"])
        cycle_runtime = int(d["cycle_runtime"])
        forecast_hour = int(d["forecast_hour"])
        region = Region(d["region"])
        product = Product(d["product"])

        return cls(
            date=date,
            category=category,
            cycle_runtime=cycle_runtime,
            forecast_hour=forecast_hour,
            region=region,
            product=product,
        )

    # @property
    # def filename(self) -> str:
    #     # reconstruct it
    #     ...

    @property
    def id(self) -> str:
        return "-".join(
            [
                self.date.strftime("%Y%m%d"),
                self.category,
                self.region,
                self.product,
                str(self.cycle_runtime),
                str(self.forecast_hour),
            ]
        )

    @property
    def datetime(self) -> datetime.datetime:
        # TODO: confirm this is correct
        return self.date + datetime.timedelta(hours=self.forecast_hour)

    @property
    def extra_properties(self) -> dict[str, str | int]:
        # TODO: use the forecast extension
        return {
            "nwm:category": self.category.value,
            "nwm:region": self.region.value,
            "nwm:product": self.product.value,
            "nwm:forecast_hour": self.forecast_hour,
        }


def create_item(
    href: str,
    read_href_modifier: typing.Callable[[str], str] | None = None,
    kerchunk_indices: dict[str, typing.Any] | None = None,
) -> pystac.Item:
    path = "/".join(href.rsplit("/", 3)[-3:])
    info = NWMInfo.from_filename(path)

    ds = xr.open_dataset(fsspec.open(href).open())
    ds = xstac.fix_attrs(ds)

    # TODO: geometry from the region (conus, ...)
    template = pystac.Item(
        info.id,
        geometry=None,
        bbox=None,
        datetime=info.datetime,
        properties=dict(info.extra_properties),
    )

    additional_dimensions = {
        "feature_id": {
            "type": "ID",
            "description": ds.feature_id.attrs["comment"],
            "extent": [None, None],
        },
        "reference_time": {
            "type": "reference-time",
            "description": ds.reference_time.attrs["long_name"],
            "extent": [None, None],
        },
    }

    item = xstac.xarray_to_stac(
        ds,
        template,
        x_dimension=False,
        y_dimension=False,
        kerchunk_indices=kerchunk_indices,
        **additional_dimensions,
    )

    assert isinstance(item, pystac.Item)
    item.assets["data"] = pystac.Asset(href=href, media_type="application/x-netcdf")

    return item


def create_collection() -> pystac.Collection:
    return pystac.Collection()
