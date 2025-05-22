import json
from flet.core.ref import Ref
from flet.core.control import Control
from flet_health.health_data_types import *
from typing import Optional, Any
from flet.core.types import OptionalControlEventCallable
from flet_health.health_schemas import (
    StepsIntervalParams,
    HealthAuthorizationParams,
    HealthAggregateDataParams,
    GetHealthDataParams,
    HealthIntervalDataParams,
    BloodOxygenParams,
    WriteHealthDataParams,
    WorkoutParams,
    BloodPressureParams,
    MealParams,
    AudiogramParams,
    MenstrualFlowParams,
    InsulinDeliveryParams,
    RemoveDuplicatesParams, DeleteParams, DeleteByUUIDParams
)


class Health(Control):
    """
    A control that lets you read and write health data to and from Apple Health and Google Health Connect.
    This control is not visual and must be added to the `page.overlay` list.

    Note: Google has deprecated the Google Fit API. According to the documentation, as of May 1st 2024 developers cannot
    sign up for using the API. As such, this package has removed support for Google Fit as of version 11.0.0 and users
    are urged to upgrade as soon as possible.

    More: https://pub.dev/packages/health
    """

    def __init__(
            self,
            # Control
            #
            ref: Optional[Ref] = None,
            data: Any = None,
            on_error: OptionalControlEventCallable = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.on_error = on_error

    def _get_control_name(self):
        return "flet_health"

    def request_health_data_history_authorization(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Requests the Health Data History permission.

        See this for more info:
            https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()

            Android only. Returns true on iOS or false if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="request_health_data_history_authorization",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def request_health_data_history_authorization_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Requests the Health Data History permission.

        See this for more info:
            https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()

            Android only. Returns True on iOS or False if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = await self.invoke_method_async(
            method_name="request_health_data_history_authorization",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def is_health_data_history_available(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks if the Health Data History feature is available.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()
        Android only. Returns False on iOS or if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="is_health_data_history_available",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def is_health_data_history_available_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks if the Health Data History feature is available.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()
        Android only. Returns False on iOS or if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="is_health_data_history_available_async",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def is_health_data_history_authorized(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks the current status of the Health Data History permission.
        Make sure to check [is_health_connect_available] before calling this method.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()
        Android only. Returns True on iOS or False if an error occurs.

        :return: True if successful, False otherwise.

        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="is_health_data_history_authorized",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def is_health_data_history_authorized_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks the current status of the Health Data History permission.
        Make sure to check [is_health_connect_available] before calling this method.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_HISTORY()
        Android only. Returns True on iOS or False if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method_async(
            method_name="is_health_data_history_authorized",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def is_health_data_in_background_available(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks if the Health Data in Background feature is available.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND()
        Android only. Returns false on iOS or if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="is_health_data_in_background_available",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def is_health_data_in_background_available_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Checks if the Health Data in Background feature is available.

        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND()
        Android only. Returns false on iOS or if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method_async(
            method_name="is_health_data_in_background_available",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def request_health_data_in_background_authorization(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Requests the Health Data in Background permission.
        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND()
        Android only. Returns True on iOS or False if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="request_health_data_in_background_authorization",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def request_health_data_in_background_authorization_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Requests the Health Data in Background permission.
        See this for more info: https://developer.android.com/reference/androidx/health/connect/client/permission/HealthPermission#PERMISSION_READ_HEALTH_DATA_IN_BACKGROUND()
        Android only. Returns True on iOS or False if an error occurs.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = await self.invoke_method_async(
            method_name="request_health_data_in_background_authorization",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def request_authorization(self, params: HealthAuthorizationParams) -> bool:
        """
        Requests permissions to access health data specified in `types`.

        Returns `True` if the request is successful, `False` otherwise.

        :param params: HealthAuthorizationParams
        :param types: (list) List of health data types for which permissions are requested.
        :param data_access: (list, optional)
            - If not specified, each data type in `types` will be requested with READ permission (`HealthDataAccess.READ`).
            - If specified, each entry in `data_access` must correspond to the respective index in `types`.
            Additionally, the length of `permissions` must be equal to that of `types`.
        :param wait_timeout: (float, optional) Maximum time to wait for the permission request to complete.

        Notes:
                - This function may block execution if permissions have already been granted.
            Therefore, it is recommended to check `has_permissions()` before calling it.
                - On iOS, due to Apple HealthKit's privacy restrictions, it is not possible to determine
            whether READ access has been granted. Therefore, this function will return **True if the
            permission request window was displayed to the user without errors**, when called with
            READ or READ/WRITE permissions.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="request_authorization",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def request_authorization_async(self, params: HealthAuthorizationParams) -> bool:
        """
        Requests permissions to access health data specified in `types`.

        Returns `True` if the request is successful, `False` otherwise.

        :param params: HealthAuthorizationParams
        :param types: (list) List of health data types for which permissions are requested.
        :param data_access: (list, optional)
            - If not specified, each data type in `types` will be requested with READ permission (`HealthDataAccess.READ`).
            - If specified, each entry in `data_access` must correspond to the respective index in `types`.
            Additionally, the length of `permissions` must be equal to that of `types`.
        :param wait_timeout: (float, optional) Maximum time to wait for the permission request to complete.

        Notes:
                - This function may block execution if permissions have already been granted.
            Therefore, it is recommended to check `has_permissions()` before calling it.
                - On iOS, due to Apple HealthKit's privacy restrictions, it is not possible to determine
            whether READ access has been granted. Therefore, this function will return **True if the
            permission request window was displayed to the user without errors**, when called with
            READ or READ/WRITE permissions.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="request_authorization",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    def has_permissions(self, params: HealthAuthorizationParams) -> Optional[bool]:
        """
        Checks if the provided health data types have the specified access permissions.

        Notes:
            - On iOS, HealthKit does not disclose if read access has been granted, so the function may return 'None'.
            - On Android, it always returns 'True' or 'False' based on the granted permissions.

        :param params: HealthAuthorizationParams
        :param types: List of 'TypesActivities, WorkoutTypes, str', representing the health data types to be checked.
        :param data_access: Optional list of 'DataAccess' corresponding to each 'type'.
                - If 'None', the function assumes 'READ' for all types.
                - If provided, it must have the same size as 'types', corresponding to each entry.
        :param wait_timeout: Maximum time to wait for the permission request to complete.

        :return:
            - True: if all the data types have the specified permissions.
            - False: if any of the data types does not have the specified permission.
            - None: if it is not possible to determine the permissions (as in iOS).
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="has_permissions",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            return None

    async def has_permissions_async(self, params: HealthAuthorizationParams) -> Optional[bool]:
        """
        Checks if the provided health data types have the specified access permissions.

        Notes:
            - On iOS, HealthKit does not disclose if read access has been granted, so the function may return 'None'.
            - On Android, it always returns 'True' or 'False' based on the granted permissions.

        :param params: HealthAuthorizationParams
        :param types: List of 'TypesActivities, WorkoutTypes, str', representing the health data types to be checked.
        :param data_access: Optional list of 'DataAccess' corresponding to each 'type'.
                - If 'None', the function assumes 'READ' for all types.
                - If provided, it must have the same size as 'types', corresponding to each entry.
        :param wait_timeout: Maximum time to wait for the permission request to complete.

        :return:
            True: if all the data types have the specified permissions.
            False: if any of the data types does not have the specified permission.
            None: if it is not possible to determine the permissions (as in iOS).
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="has_permissions",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            return None

    def revoke_permissions(self) -> None:
        """
        Revokes Google Health Connect permissions on Android of all types.

        NOTE: The app must be completely killed and restarted for the changes to take effect.

        Not implemented on iOS as there is no way to programmatically remove access.
        Android only. On iOS this does nothing.
        """

        platform = self.page.platform.value

        if platform == 'android':
            self.invoke_method(
                method_name="revoke_permissions"
            )

    def is_health_connect_available(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Is Google Health Connect available on this phone?
        Android only. Returns always true on iOS.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method(
            method_name="is_health_connect_available",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    async def is_health_connect_available_async(self, wait_timeout: Optional[float] = 25) -> bool:
        """
        Is Google Health Connect available on this phone?
        Android only. Returns always true on iOS.

        :return: True if successful, False otherwise.
        """

        platform = self.page.platform.value

        if platform == 'ios':
            return True

        result = self.invoke_method_async(
            method_name="is_health_connect_available",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        return result == 'true'

    def install_health_connect(self) -> None:
        """Prompt the user to install the Google Health Connect app via the installed store (most likely Play Store).
        Android only. On iOS this does nothing."""

        platform = self.page.platform.value

        if platform == 'android':
            self.invoke_method(method_name="install_health_connect")

    def get_health_connect_sdk_status(self, wait_timeout: Optional[float] = 25) -> Optional[HealthConnectSdkStatus]:
        """Checks the current status of Health Connect availability.

        See this for more info:
            https://developer.android.com/reference/kotlin/androidx/health/connect/client/HealthConnectClient#getSdkStatus(android.content.Context,kotlin.String)

        Android only. Returns None on iOS or if an error occurs.

        :return: HealthConnectSdkStatus enum value, or None if not on Android or on error.
        """

        platform = self.page.platform.value

        if platform != 'android':
            return HealthConnectSdkStatus.SDK_UNAVAILABLE

        try:
            result = self.invoke_method(
                method_name="get_health_connect_sdk_status",
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            if isinstance(result, str):
                return HealthConnectSdkStatus.from_string(result)

            return HealthConnectSdkStatus.SDK_UNAVAILABLE

        except Exception as error:
            print(f"Exception in get_health_connect_sdk_status_async(): {error}")
            return None

    async def get_health_connect_sdk_status_async(self, wait_timeout: Optional[float] = 25) -> Optional[HealthConnectSdkStatus]:
        """Checks the current status of Health Connect availability.

        See this for more info:
            https://developer.android.com/reference/kotlin/androidx/health/connect/client/HealthConnectClient#getSdkStatus(android.content.Context,kotlin.String)

        Android only. Returns None on iOS or if an error occurs.

        :return: HealthConnectSdkStatus enum value, or None if not on Android or on error.
        """

        platform = self.page.platform.value

        if platform != 'android':
            return None

        try:
            result = await self.invoke_method_async(
                method_name="get_health_connect_sdk_status",
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            if isinstance(result, str):
                return HealthConnectSdkStatus.from_string(result)

            return HealthConnectSdkStatus.SDK_UNAVAILABLE

        except Exception as error:
            print(f"Exception in get_health_connect_sdk_status_async(): {error}")
            return None


    def get_total_steps_in_interval(self, params: StepsIntervalParams):
        """
        Get the total number of steps within a specific time period.

        :return: `None` if not successful
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="get_total_steps_in_interval",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return int(result) if result else None

    async def get_total_steps_in_interval_async(self, params: StepsIntervalParams):
        """
        Get the total number of steps within a specific time period.

        :return: `None` if not successful
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="get_total_steps_in_interval",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return int(result) if result else None

    def get_health_aggregate_data_from_types(self, params: HealthAggregateDataParams) -> list[dict]:
        """
        Fetch a list of health data points based on [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType]
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="get_health_aggregate_data_from_types",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return json.loads(result or "[]")

    async def get_health_aggregate_data_from_types_async(
            self, params: HealthAggregateDataParams) -> list[dict]:
        """
        Fetch a list of health data points based on [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType]
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="get_health_aggregate_data_from_types",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return json.loads(result or "[]")

    def get_health_data_from_types(self, params: GetHealthDataParams) -> str | list[Any] | None:
        """
        Fetches a list of health data points based on types [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType].
        You can also specify the [recording_methods_to_filter] to filter the data points.
        If not specified, all data points will be included.

        :param wait_timeout:
        :param types: A list of HealthDataType enum values to retrieve data for.
        :param start_time: The start time for the data query.
        :param end_time: The end time for the data query.
        :param recording_method: An optional list of RecordingMethod strings to filter by.  Valid values: 'unknown', 'active', 'automatic', 'manual'.

        :return: A string representation of the health data, likely in JSON format.  The format will match what's returned by the Dart plugin.  Returns [] if no data found or an error occurred.
        """

        try:
            data = params.to_wrapped()

            # Call the native method
            result = self.invoke_method(
                method_name="get_health_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=params.wait_timeout
            )

            return json.loads(result or "[]")

        except Exception as error:
            print(f"Error in get_health_data_from_types: {error}")
            return []

    async def get_health_data_from_types_async(self, params: GetHealthDataParams) -> str | list[Any] | None:
        """
        Fetches a list of health data points based on types [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType].
        You can also specify the [recording_methods_to_filter] to filter the data points.
        If not specified, all data points will be included.

        :param wait_timeout:
        :param types: A list of HealthDataType enum values to retrieve data for.
        :param start_time: The start time for the data query.
        :param end_time: The end time for the data query.
        :param recording_method: An optional list of RecordingMethod strings to filter by.  Valid values: 'unknown', 'active', 'automatic', 'manual'.

        :return: A string representation of the health data, likely in JSON format.  The format will match what's returned by the Dart plugin.  Returns [] if no data found or an error occurred.
        """

        try:
            data = params.to_wrapped()

            # Call the native method
            result = await self.invoke_method_async(
                method_name="get_health_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=params.wait_timeout
            )

            return json.loads(result or "[]")

        except Exception as error:
            print(f"Error in get_health_data_from_types: {error}")
            return []

    def get_health_interval_data_from_types(self, params: HealthIntervalDataParams) -> list[Any]:
        """
        Fetch a list of health data points based on types [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType].
        You can also specify the [recordingMethodsToFilter] to filter the data points.
        If not specified, all data points will be included.

        :param start_time: The start time for the data query.
        :param end_time: The end time for the data query.
        :param types: A list of HealthDataType enum values to retrieve data for.
        :param interval:
        :param recording_method: An optional list of RecordingMethod strings to filter by.  Valid values: 'unknown', 'active', 'automatic', 'manual'.
        :param wait_timeout:

        :return: A string representation of the health data, likely in JSON format.  The format will match what's returned by the Dart plugin.  Returns [] if no data found or an error occurred.
        """

        try:

            data = params.to_wrapped()

            # Call the native method
            result = self.invoke_method(
                method_name="get_health_interval_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=params.wait_timeout
            )

            return json.loads(result or "[]")

        except Exception as e:
            print(f"Error in get_health_interval_data_from_types: {e}")
            return []

    async def get_health_interval_data_from_types_async(self, params: HealthIntervalDataParams) -> list[Any]:
        """
        Fetch a list of health data points based on types [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType].
        You can also specify the [recordingMethodsToFilter] to filter the data points.
        If not specified, all data points will be included.

        :param start_time: The start time for the data query.
        :param end_time: The end time for the data query.
        :param types: A list of HealthDataType enum values to retrieve data for.
        :param interval:
        :param recording_method: An optional list of RecordingMethod strings to filter by.  Valid values: 'unknown', 'active', 'automatic', 'manual'.
        :param wait_timeout:

        :return: A string representation of the health data, likely in JSON format.  The format will match what's returned by the Dart plugin.  Returns [] if no data found or an error occurred.
        """

        try:
            data = params.to_wrapped()

            # Call the native method
            result = await self.invoke_method_async(
                method_name="get_health_interval_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=params.wait_timeout
            )

            return json.loads(result or "[]")

        except Exception as e:
            print(f"Error in get_health_interval_data_from_types: {e}")
            return []

    def write_blood_oxygen(self, params: BloodOxygenParams) -> bool:
        """
        Saves blood oxygen saturation record.

        :return: True if successful, False otherwise
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_blood_oxygen",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    async def write_blood_oxygen_async(self, params: BloodOxygenParams) -> bool:
        """
        Saves blood oxygen saturation record.

        :return: True if successful, False otherwise
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_blood_oxygen",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    def write_health_data(self, params: WriteHealthDataParams) -> bool:
        """
        Writes generic health data.

        :param: value (float): The health data's value as a floating-point number.
        :param: start_time (datetime): The start time when this value is measured.
                Must be equal to or earlier than end_time.
        :param: end_time (datetime): The end time when this value is measured.
                Must be equal to or later than start_time.  Simply set end_time
                equal to start_time if the value is measured only at a specific
                point in time (default).
        :param: types (HealthDataTypeAndroid | HealthDataTypeIOS): The value's
                HealthDataType.
        :param: unit (HealthDataUnit, optional): The unit the health data is measured in.
                Defaults to None.  This parameter is primarily relevant for iOS.
        :param: recording_method (RecordingMethod, optional): The recording
                method of the data point.  Defaults to RecordingMethod.AUTOMATIC.
                On iOS, this must be RecordingMethod.MANUAL or
                RecordingMethod.AUTOMATIC.
        :param: wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        Values for Sleep and Headache are ignored and will be automatically
        assigned the default value.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_health_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def write_health_data_async(self, params: WriteHealthDataParams) -> bool:
        """
        Writes generic health data.

        :param: value (float): The health data's value as a floating-point number.
        :param: start_time (datetime): The start time when this value is measured.
                Must be equal to or earlier than end_time.
        :param: end_time (datetime): The end time when this value is measured.
                Must be equal to or later than start_time.  Simply set end_time
                equal to start_time if the value is measured only at a specific
                point in time (default).
        :param: types (HealthDataTypeAndroid | HealthDataTypeIOS): The value's
                HealthDataType.
        :param: unit (HealthDataUnit, optional): The unit the health data is measured in.
                Defaults to None.  This parameter is primarily relevant for iOS.
        :param: recording_method (RecordingMethod, optional): The recording
                method of the data point.  Defaults to RecordingMethod.AUTOMATIC.
                On iOS, this must be RecordingMethod.MANUAL or
                RecordingMethod.AUTOMATIC.
        :param: wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        Values for Sleep and Headache are ignored and will be automatically
        assigned the default value.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_health_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    def write_workout_data(self, params: WorkoutParams) -> bool:
        """
        Write workout data to Apple Health or Google Health Connect.

        :return: True if the workout data was successfully added.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_workout_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    async def write_workout_data_async(self, params: WorkoutParams) -> bool:
        """
        Write workout data to Apple Health or Google Health Connect.

        :return: True if the workout data was successfully added.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_workout_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    def write_blood_pressure(self, params: BloodPressureParams) -> bool:
        """
        Saves a blood pressure record.

        :return: True if successful, false otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_blood_pressure",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    async def write_blood_pressure_async(self, params: BloodPressureParams) -> bool:
        """
        Saves a blood pressure record.

        :return: True if successful, false otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_blood_pressure",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    def write_meal(self, params: MealParams) -> bool:
        """
        Saves meal record into Apple Health or Health Connect.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_meal",  # The key name for the flutter case
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def write_meal_async(self, params: MealParams) -> bool:
        """
        Saves meal record into Apple Health or Health Connect.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_meal",  # The key name for the flutter case
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    def write_audiogram(self, params: AudiogramParams) -> bool:
        """
        Saves audiogram into Apple Health. Not supported on Android.

        :return: True if successful, false otherwise.
        """

        platform = self.page.platform.value

        if platform == 'android':
            raise ValueError('writeAudiogram is not supported on Android')

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_audiogram",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    async def write_audiogram_async(
            self, params: AudiogramParams) -> bool:
        """
        Saves audiogram into Apple Health. Not supported on Android.

        :return: True if successful, false otherwise.
        """

        platform = self.page.platform.value

        if platform == 'android':
            raise ValueError('writeAudiogram is not supported on Android')

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_audiogram",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    def write_menstruation_flow(self, params: MenstrualFlowParams) -> bool:
        """
        Save menstruation flow into Apple Health and Google Health Connect.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_menstruation_flow",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    async def write_menstruation_flow_async(
            self, params: MenstrualFlowParams) -> bool:
        """
        Save menstruation flow into Apple Health and Google Health Connect.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_menstruation_flow",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )
        return result == "true"

    def write_insulin_delivery(self, params: InsulinDeliveryParams):
        """
        Saves insulin delivery record into Apple Health.
        Returns true if successful, false otherwise.

        :param units: - the number of units of insulin taken.
        :param reason: - the insulin reason, basal or bolus.
        :param start_time: - the start time when the meal was consumed.
        :param end_time: - the end time when the meal was consumed. It must be equal to or earlier than [end_time].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="write_insulin_delivery",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def write_insulin_delivery_async(self, params: InsulinDeliveryParams):
        """
        Saves insulin delivery record into Apple Health.
        Returns true if successful, false otherwise.

        :param units: - the number of units of insulin taken.
        :param reason: - the insulin reason, basal or bolus.
        :param start_time: - the start time when the meal was consumed.
        :param end_time: - the end time when the meal was consumed. It must be equal to or earlier than [end_time].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="write_insulin_delivery",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    def remove_duplicates(self, params: RemoveDuplicatesParams) -> list[dict]:
        """
        Removes duplicate HealthDataPoint entries using the Dart side method.

        :param points: A list of HealthDataPoint dictionaries (JSON format).
        :param wait_timeout: Timeout in seconds to wait for the method result.
        :return: A list of deduplicated HealthDataPoint dictionaries.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="remove_duplicates",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return json.loads(result or "[]")

    async def remove_duplicates_async(self, params: RemoveDuplicatesParams) -> list[dict]:
        """
        Asynchronously removes duplicate HealthDataPoint entries using the Dart side method.

        :param points: A list of HealthDataPoint dictionaries (JSON format).
        :param wait_timeout: Timeout in seconds to wait for the method result.
        :return: A list of deduplicated HealthDataPoint dictionaries.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="remove_duplicates",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return json.loads(result or "[]")

    def delete(self, params: DeleteParams) -> bool:
        """
        Deletes all records of the given [type] for a given period of time.

        :param types: - the value's HealthDataType.
        :param start_time: - the start time when this [value] is measured. Must be equal to or earlier than [endTime].
        :param end_time: - the end time when this [value] is measured. Must be equal to or later than [startTime].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def delete_async(self, params: DeleteParams) -> bool:
        """
        Deletes all records of the given [type] for a given period of time.

        :param types: - the value's HealthDataType.
        :param start_time: - the start time when this [value] is measured. Must be equal to or earlier than [endTime].
        :param end_time: - the end time when this [value] is measured. Must be equal to or later than [startTime].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    def delete_by_uuid(self, params: DeleteByUUIDParams) -> bool:
        """
        Deletes a specific health record by its UUID.

        :param uuid: - The UUID of the health record to delete.
        :param types: - The health data type of the record. Required on iOS.
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        On Android, only the UUID is required. On iOS, both UUID and type are required.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = self.invoke_method(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    async def delete_by_uuid_async(self, params: DeleteByUUIDParams) -> bool:
        """
        Deletes a specific health record by its UUID.

        :param uuid: - The UUID of the health record to delete.
        :param types: - The health data type of the record. Required on iOS.
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        On Android, only the UUID is required. On iOS, both UUID and type are required.

        :return: True if successful, False otherwise.
        """

        data = params.to_wrapped()

        result = await self.invoke_method_async(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=params.wait_timeout
        )

        return result == "true"

    @property
    def on_error(self) -> OptionalControlEventCallable:
        return self._get_attr("error")

    @on_error.setter
    def on_error(self, handler: OptionalControlEventCallable):
        self._add_event_handler("error", handler)
