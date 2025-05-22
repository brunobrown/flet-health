import json
from datetime import datetime
from typing import Optional, List, Union, Any, Dict
from pydantic import BaseModel, Field, root_validator

from .health_data_types import (
    HealthDataTypeAndroid,
    HealthDataTypeIOS,
    HealthWorkoutActivityType,
    HealthDataUnit,
    RecordingMethod,
    MealType,
    DataAccess,
    MenstrualFlow,
    InsulinDeliveryReason
)
from .utils import wrap_value


class WrappedBaseModel(BaseModel):
    force_wrap: dict = Field(default_factory=dict)

    def to_wrapped(self) -> str:
        wrapped = {
            key: wrap_value(
                value,
                **self.force_wrap.get(key, {})
            )
            for key, value in self.dict(exclude={"force_wrap"}).items()
        }
        return json.dumps(wrapped)


class HealthAuthorizationParams(WrappedBaseModel):
    types: List[Union[HealthDataTypeAndroid, HealthDataTypeIOS, HealthWorkoutActivityType]]
    data_access: Optional[List[DataAccess]] = None
    wait_timeout: float = Field(default=25, gt=0)

    @root_validator(pre=True)
    def apply_default_data_access(cls, values):
        types = values.get('types')
        data_access = values.get('data_access')

        if data_access is None:
            values['data_access'] = [DataAccess.READ] * len(types)

        return values


class StepsIntervalParams(WrappedBaseModel):
    start_time: datetime
    end_time: datetime
    include_manual_entry: Optional[bool] = True
    wait_timeout: float = Field(default=25, gt=0)


class HealthAggregateDataParams(WrappedBaseModel):
    types: List[Union[HealthDataTypeAndroid, HealthDataTypeIOS, HealthWorkoutActivityType]]
    start_time: datetime
    end_time: datetime
    activity_segment_duration: Optional[int] = 1
    include_manual_entry: Optional[bool] = True
    wait_timeout: float = Field(default=25, gt=0)


class HealthIntervalDataParams(WrappedBaseModel):
    start_time: datetime
    end_time: datetime
    types: List[Union[HealthDataTypeAndroid, HealthDataTypeIOS, HealthWorkoutActivityType]]
    interval: int
    recording_method: Optional[List[RecordingMethod]] = None
    wait_timeout: float = Field(default=25, gt=0)

    @root_validator(pre=True)
    def set_defaults_and_metadata(cls, values):
        if 'recording_method' not in values or values['recording_method'] is None:
            values['recording_method'] = []

            force_wrap = values.get('force_wrap', {})
            force_wrap['recording_method'] = {
                "type_name": "list",
                "subtype_name": "enum",
                "class_name": "RecordingMethod"
            }
            values['force_wrap'] = force_wrap

        return values


class BloodOxygenParams(WrappedBaseModel):
    saturation: float
    start_time: datetime
    end_time: datetime
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class BloodPressureParams(WrappedBaseModel):
    systolic: int
    diastolic: int
    start_time: datetime
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class WriteHealthDataParams(WrappedBaseModel):
    value: float
    start_time: datetime
    end_time: datetime
    types: Union[HealthDataTypeAndroid, HealthDataTypeIOS]
    unit: HealthDataUnit = HealthDataUnit.NO_UNIT
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class GetHealthDataParams(WrappedBaseModel):
    types: List[Union[HealthDataTypeAndroid, HealthDataTypeIOS, HealthWorkoutActivityType]]
    start_time: datetime
    end_time: datetime
    recording_method: Optional[List[RecordingMethod]] = None
    wait_timeout: float = Field(default=25, gt=0)

    @root_validator(pre=True)
    def set_defaults_and_metadata(cls, values):
        if 'recording_method' not in values or values['recording_method'] is None:
            values['recording_method'] = []

            force_wrap = values.get('force_wrap', {})
            force_wrap['recording_method'] = {
                "type_name": "list",
                "subtype_name": "enum",
                "class_name": "RecordingMethod"
            }
            values['force_wrap'] = force_wrap

        return values


class WorkoutParams(WrappedBaseModel):
    activity_type: HealthWorkoutActivityType
    start_time: datetime
    end_time: datetime
    total_energy_burned: Optional[int] = None
    total_energy_burned_unit: HealthDataUnit = HealthDataUnit.KILOCALORIE
    total_distance: Optional[int] = None
    total_distance_unit: HealthDataUnit = HealthDataUnit.METER
    title: Optional[str] = None
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class MealParams(WrappedBaseModel):
    meal_type: MealType
    start_time: datetime
    end_time: datetime
    calories_consumed: Optional[float] = None
    carbohydrates: Optional[float] = None
    protein: Optional[float] = None
    fat_total: Optional[float] = None
    name: Optional[str] = None
    caffeine: Optional[float] = None
    vitamin_a: Optional[float] = None
    b1_thiamin: Optional[float] = None
    b2_riboflavin: Optional[float] = None
    b3_niacin: Optional[float] = None
    b5_pantothenic_acid: Optional[float] = None
    b6_pyridoxine: Optional[float] = None
    b7_biotin: Optional[float] = None
    b9_folate: Optional[float] = None
    b12_cobalamin: Optional[float] = None
    vitamin_c: Optional[float] = None
    vitamin_d: Optional[float] = None
    vitamin_e: Optional[float] = None
    vitamin_k: Optional[float] = None
    calcium: Optional[float] = None
    cholesterol: Optional[float] = None
    chloride: Optional[float] = None
    chromium: Optional[float] = None
    copper: Optional[float] = None
    fat_unsaturated: Optional[float] = None
    fat_monounsaturated: Optional[float] = None
    fat_polyunsaturated: Optional[float] = None
    fat_saturated: Optional[float] = None
    fat_trans_monoenoic: Optional[float] = None
    fiber: Optional[float] = None
    iodine: Optional[float] = None
    iron: Optional[float] = None
    magnesium: Optional[float] = None
    manganese: Optional[float] = None
    molybdenum: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    selenium: Optional[float] = None
    sodium: Optional[float] = None
    sugar: Optional[float] = None
    water: Optional[float] = None
    zinc: Optional[float] = None
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class AudiogramParams(WrappedBaseModel):
    frequencies: List[float]
    left_ear_sensitivities: List[float]
    right_ear_sensitivities: List[float]
    start_time: datetime
    end_time: datetime
    metadata: Optional[Dict[str, Any]] = None
    wait_timeout: float = Field(default=25, gt=0)


class MenstrualFlowParams(WrappedBaseModel):
    flow: MenstrualFlow
    start_time: datetime
    end_time: datetime
    is_start_of_cycle: bool
    recording_method: RecordingMethod = RecordingMethod.UNKNOWN
    wait_timeout: float = Field(default=25, gt=0)


class InsulinDeliveryParams(WrappedBaseModel):
    units: float
    reason: InsulinDeliveryReason
    start_time: datetime
    end_time: datetime
    wait_timeout: float = Field(default=25, gt=0)


class RemoveDuplicatesParams(WrappedBaseModel):
    points: List[Dict[str, Any]]
    wait_timeout: float = Field(default=25, gt=0)

    class Config:
        json_schema_extra = {
            "example": [
               {
                  "uuid":"69715ead-9074-491e-8d30-83a75f1fb33b",
                  "value":{
                     "__type":"NumericHealthValue",
                     "numericValue":250.0
                  },
                  "type":"TOTAL_CALORIES_BURNED",
                  "unit":"KILOCALORIE",
                  "dateFrom":"2025-04-30T21:04:10.514",
                  "dateTo":"2025-04-30T21:34:10.514",
                  "sourcePlatform":"googleHealthConnect",
                  "sourceDeviceId":"unknown",
                  "sourceId":"",
                  "sourceName":"com.flet.health_lib_test",
                  "recordingMethod":"automatic"
               },
               {
                  "uuid":"69715ead-9074-491e-8d30-83a75f1fb33b",
                  "value":{
                     "__type":"NumericHealthValue",
                     "numericValue":250.0
                  },
                  "type":"TOTAL_CALORIES_BURNED",
                  "unit":"KILOCALORIE",
                  "dateFrom":"2025-04-30T21:04:10.514",
                  "dateTo":"2025-04-30T21:34:10.514",
                  "sourcePlatform":"googleHealthConnect",
                  "sourceDeviceId":"unknown",
                  "sourceId":"",
                  "sourceName":"com.flet.health_lib_test",
                  "recordingMethod":"automatic"
               }
            ]
        }


class DeleteParams(WrappedBaseModel):
    types: HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType
    start_time: datetime
    end_time: Optional[datetime] = None
    wait_timeout: float = Field(default=25, gt=0)


class DeleteByUUIDParams(WrappedBaseModel):
    uuid: str
    types: Optional[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType] = None,
    wait_timeout: float = Field(default=25, gt=0)
