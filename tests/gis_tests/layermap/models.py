from django.contrib.gis.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class NamedModel(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class State(NamedModel):
    pass


class County(NamedModel):
    state = models.ForeignKey(State, models.CASCADE)
    mpoly = models.MultiPolygonField(srid=4269)  # Multipolygon in NAD83


class CountyFeat(NamedModel):
    poly = models.PolygonField(srid=4269)


class City(NamedModel):
    name_txt = models.TextField(default='')
    name_short = models.CharField(max_length=5)
    population = models.IntegerField()
    density = models.DecimalField(max_digits=7, decimal_places=1)
    dt = models.DateField()
    point = models.PointField()

    class Meta:
        app_label = 'layermap'


class Interstate(NamedModel):
    length = models.DecimalField(max_digits=6, decimal_places=2)
    path = models.LineStringField()

    class Meta:
        app_label = 'layermap'


# Same as `City` above, but for testing model inheritance.
class CityBase(NamedModel):
    population = models.IntegerField()
    density = models.DecimalField(max_digits=7, decimal_places=1)
    point = models.PointField()


class ICity1(CityBase):
    dt = models.DateField()

    class Meta(CityBase.Meta):
        pass


class ICity2(ICity1):
    dt_time = models.DateTimeField(auto_now=True)

    class Meta(ICity1.Meta):
        pass


class Invalid(models.Model):
    point = models.PointField()


class HasNulls(models.Model):
    uuid = models.CharField(primary_key=True, editable=False, max_length=36)
    geom = models.PolygonField(srid=4326, blank=True, null=True)
    fill_color = models.CharField(blank=False, null=False, max_length=20)
    name = models.CharField(blank=True, null=True, max_length=20)
    fill_opacity = models.FloatField(blank=False, null=False)
    some_number = models.FloatField(blank=True, null=True)


# Mapping dictionaries for the models above.
co_mapping = {
    'name': 'Name',
    # ForeignKey's use another mapping dictionary for the _related_ Model (State in this case).
    'state': {'name': 'State'},
    'mpoly': 'MULTIPOLYGON',  # Will convert POLYGON features into MULTIPOLYGONS.
}

cofeat_mapping = {'name': 'Name',
                  'poly': 'POLYGON',
                  }

city_mapping = {'name': 'Name',
                'population': 'Population',
                'density': 'Density',
                'dt': 'Created',
                'point': 'POINT',
                }

inter_mapping = {'name': 'Name',
                 'length': 'Length',
                 'path': 'LINESTRING',
                 }

has_nulls_mapping = {'geom': 'POLYGON',
                     'uuid': 'UUID',
                     'fill_color': 'FILL_COLOR',
                     'name': 'NAME',
                     'fill_opacity': 'FILL_OPACI',
                     'some_number': 'SOME_NUMBE',
                     }
