import json
from datetime import datetime
from flet.core.ref import Ref
from flet.core.control import Control
from flet_health.health_data_types import *
from typing import Optional, Any, List, Dict
from flet.core.types import OptionalControlEventCallable


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

    def request_permission(self, permission: Permissions, wait_timeout: Optional[float] = 25) -> PermissionStatus:
        """
        Requests permission on devices Android 10+ (API 29+).

        This method sends a request to access activity recognition data. He waits for a response indicating
        whether permission was granted or denied

        :arg permission: (Permissions): The specific activity permission to request
        :arg wait_timeout: (Optional[float]): The maximum time (in seconds) to wait for a response. Default is 25 seconds.

        :return:
            str: The result of the permission request.
            It can be one of the following states: "granted", "denied", or "permanentlyDenied".

        :raise ValueError: If `permission` is not an instance of `Permissions`.
        """

        if not isinstance(permission, Permissions):
            raise ValueError("'Permission' must be an instance of 'Permissions'.")

        data_str = json.dumps({"permission": permission.value})

        result = self.invoke_method(
            method_name='request_permission',
            arguments={'data': data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return PermissionStatus(result) if result is not None else None

    async def request_permission_async(self, permission: Permissions, wait_timeout: Optional[float] = 25) -> PermissionStatus:
        """
        Requests permission on Android devices Android 10+ (API 29+).

        This method sends a request to access activity recognition data. He waits for a response indicating
        whether permission was granted or denied

        :arg permission: (Permissions): The specific activity permission to request
        :arg wait_timeout: (Optional[float]): The maximum time (in seconds) to wait for a response. Default is 25 seconds.

        :return:
            str: The result of the permission request.
            It can be one of the following states: "granted", "denied", or "permanentlyDenied".

        :raise ValueError: If `permission` is not an instance of `Permissions`.
        """

        if not isinstance(permission, Permissions):
            raise ValueError("'Permission' must be an instance of 'Permissions'.")

        data_str = json.dumps({"permission": permission.value})

        result = await self.invoke_method_async(
            method_name='request_permission',
            arguments={'data': data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return PermissionStatus(result) if result is not None else None

    def request_multiple_permissions(
            self, permissions: List[Permissions], wait_timeout: Optional[float] = 25
    ) -> dict[str, PermissionStatus]:
        """
        Requests multiple permissions on the device.

        :param permissions: List of Permissions enums.
        :param wait_timeout: Time to wait for result (in seconds).
        :return: Dictionary mapping each permission to its PermissionStatus.
        :raises ValueError: If any item is not an instance of Permissions.
        """

        if not all(isinstance(p, Permissions) for p in permissions):
            raise ValueError("All items in 'permissions' must be instances of 'Permissions'.")

        data_str = json.dumps({"permissions": [p.value for p in permissions]})

        result = self.invoke_method(
            method_name="request_multiple_permissions",
            arguments={"data": data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        if result is None:
            return {}

        result_dict = json.loads(result)
        return {
            perm_name: PermissionStatus(status)
            for perm_name, status in result_dict.items()
        }

    async def request_multiple_permissions_async(
            self, permissions: List[Permissions], wait_timeout: Optional[float] = 25
    ) -> dict[str, PermissionStatus]:
        """
        Requests multiple permissions on the device.

        :param permissions: List of Permissions enums.
        :param wait_timeout: Time to wait for result (in seconds).
        :return: Dictionary mapping each permission to its PermissionStatus.
        :raises ValueError: If any item is not an instance of Permissions.
        """

        if not all(isinstance(p, Permissions) for p in permissions):
            raise ValueError("All items in 'permissions' must be instances of 'Permissions'.")

        data_str = json.dumps({"permissions": [p.value for p in permissions]})

        result = await self.invoke_method_async(
            method_name="request_multiple_permissions",
            arguments={"data": data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

        if result is None:
            return {}

        result_dict = json.loads(result)
        return {
            perm_name: PermissionStatus(status)
            for perm_name, status in result_dict.items()
        }

    def request_and_validate_permissions(
            self, permissions: List[Permissions], wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Requests multiple permissions and returns True if all are granted.

        :param permissions: List of Permissions enums.
        :param wait_timeout: Time to wait for result (in seconds).
        :return: True if all permissions are granted, False otherwise.
        """

        statuses = self.request_multiple_permissions(
            permissions=permissions,
            wait_timeout=wait_timeout
        )

        return all(status == PermissionStatus.GRANTED for status in statuses.values())

    async def request_and_validate_permissions_async(
            self, permissions: List[Permissions], wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Requests multiple permissions and returns True if all are granted.

        :param permissions: List of Permissions enums.
        :param wait_timeout: Time to wait for result (in seconds).
        :return: True if all permissions are granted, False otherwise.
        """

        statuses = await self.request_multiple_permissions_async(
            permissions=permissions,
            wait_timeout=wait_timeout
        )

        return all(status == PermissionStatus.GRANTED for status in statuses.values())

    def check_permission(self, permission: Permissions, wait_timeout: Optional[float] = 25) -> Optional[PermissionStatus]:
        if not isinstance(permission, Permissions):
            raise ValueError("'Permission' must be an instance of 'Permissions'.")

        data_str = json.dumps({"permission": permission.value})

        result = self.invoke_method(
            "check_permission",
            {'data': data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(result) if result is not None else None

    async def check_permission_async(self, permission: Permissions, wait_timeout: Optional[float] = 25) -> Optional[PermissionStatus]:
        if not isinstance(permission, Permissions):
            raise ValueError("'Permission' must be an instance of 'Permissions'.")

        data_str = json.dumps({"permission": permission.value})

        result = await self.invoke_method_async(
            "check_permission",
            {"data": data_str},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(result) if result is not None else None

    def open_app_settings(self, wait_timeout: Optional[float] = 25) -> bool:
        opened = self.invoke_method(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

    async def open_app_settings_async(self, wait_timeout: Optional[float] = 25) -> bool:
        opened = await self.invoke_method_async(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

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

            Android only. Returns true on iOS or false if an error occurs.

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

    def request_authorization(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            data_access: Optional[List[DataAccess]] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Requests permissions to access health data specified in `types`.

        Returns `True` if the request is successful, `False` otherwise.

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

        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        if data_access is None:
            data_access = [DataAccess.READ] * len(types)

        else:
            if not all(isinstance(da, DataAccess) for da in data_access):
                raise ValueError("All elements of 'data_access' must be instances of 'DataAccess'.")
            if len(data_access) != len(types):
                raise ValueError("The 'data_access' list must be the same size as 'types'.")

        data = json.dumps(
            {
                "types": [t.value for t in types],
                "data_access": [da.value for da in data_access] if data_access else None,
            }
        )

        result = self.invoke_method(
            method_name="request_authorization",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def request_authorization_async(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            data_access: Optional[List[DataAccess]] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Requests permissions to access health data specified in `types`.

        Returns `True` if the request is successful, `False` otherwise.

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

        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        if data_access is None:
            data_access = [DataAccess.READ] * len(types)

        else:
            if not all(isinstance(da, DataAccess) for da in data_access):
                raise ValueError("All elements of 'data_access' must be instances of 'DataAccess'.")
            if len(data_access) != len(types):
                raise ValueError("The 'data_access' list must be the same size as 'types'.")

        data = json.dumps(
            {
                "types": [t.value for t in types],
                "data_access": [da.value for da in data_access] if data_access else None,
            }
        )

        result = await self.invoke_method_async(
            method_name="request_authorization",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    def has_permissions(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            data_access: Optional[List[DataAccess]] = None,
            wait_timeout: Optional[float] = 25
    ) -> Optional[bool]:
        """
        Checks if the provided health data types have the specified access permissions.

        Notes:
            - On iOS, HealthKit does not disclose if read access has been granted, so the function may return 'None'.
            - On Android, it always returns 'True' or 'False' based on the granted permissions.

        :param types: List of 'TypesActivities, WorkoutTypes, str', representing the health data types to be checked.
        :param data_access: Optional list of 'DataAccess' corresponding to each 'type'.
                - If 'None', the function assumes 'READ' for all types.
                - If provided, it must have the same size as 'types', corresponding to each entry.

        :return:
            - True: if all the data types have the specified permissions.
            - False: if any of the data types does not have the specified permission.
            - None: if it is not possible to determine the permissions (as in iOS).
        """

        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        if data_access is None:
            data_access = [DataAccess.READ] * len(types)

        else:
            if not all(isinstance(da, DataAccess) for da in data_access):
                raise ValueError("All elements of 'data_access' must be instances of 'DataAccess'.")
            if len(data_access) != len(types):
                raise ValueError("The 'data_access' list must be the same size as 'types'.")

        data = json.dumps(
            {
                "types": [t.value for t in types],
                "data_access": [da.value for da in data_access],
            }
        )

        result = self.invoke_method(
            method_name="has_permissions",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        if result == "true":
            return True
        elif result == "false":
            return False
        else:
            return None

    async def has_permissions_async(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            data_access: Optional[List[DataAccess]] = None,
            wait_timeout: Optional[float] = 25
    ) -> Optional[bool]:
        """
        Checks if the provided health data types have the specified access permissions.

        Notes:
            - On iOS, HealthKit does not disclose if read access has been granted, so the function may return 'None'.
            - On Android, it always returns 'True' or 'False' based on the granted permissions.

        :param types: List of 'TypesActivities, WorkoutTypes, str', representing the health data types to be checked.
        :param data_access: Optional list of 'DataAccess' corresponding to each 'type'.
                - If 'None', the function assumes 'READ' for all types.
                - If provided, it must have the same size as 'types', corresponding to each entry.

        :return:
            True: if all the data types have the specified permissions.
            False: if any of the data types does not have the specified permission.
            None: if it is not possible to determine the permissions (as in iOS).
        """

        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        if data_access is None:
            data_access = [DataAccess.READ] * len(types)

        else:
            if not all(isinstance(da, DataAccess) for da in data_access):
                raise ValueError("All elements of 'data_access' must be instances of 'DataAccess'.")
            if len(data_access) != len(types):
                raise ValueError("The 'data_access' list must be the same size as 'types'.")

        data = json.dumps(
            {
                "types": [t.value for t in types],
                "data_access": [da.value for da in data_access],
            }
        )

        result = await self.invoke_method_async(
            method_name="has_permissions",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
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

    def install_health_connect(self) -> None:
        """Prompt the user to install the Google Health Connect app via the installed store (most likely Play Store).
        Android only. On iOS this does nothing."""

        platform = self.page.platform.value

        if platform == 'android':
            self.invoke_method(method_name="install_health_connect")

    def get_health_connect_sdk_status(self, wait_timeout: Optional[float] = 25) -> bool | None:
        """Checks the current status of Health Connect availability.

        See this for more info:
            https://developer.android.com/reference/kotlin/androidx/health/connect/client/HealthConnectClient#getSdkStatus(android.content.Context,kotlin.String)

        Android only. Returns null on iOS or if an error occurs.

        :return: True if the SDK is available, False if not, None if platform is not Android.
        """


        platform = self.page.platform.value

        if platform != 'android':
            return None

        result = self.invoke_method(
            method_name="get_health_connect_sdk_status",
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        if result == 'HealthConnectSdkStatus.sdkAvailable':
            return True
        else:
            return False

    async def get_health_connect_sdk_status_async(self, wait_timeout: Optional[float] = 25) -> bool | None:
        """Checks the current status of Health Connect availability.

        See this for more info:
            https://developer.android.com/reference/kotlin/androidx/health/connect/client/HealthConnectClient#getSdkStatus(android.content.Context,kotlin.String)

        Android only. Returns null on iOS or if an error occurs.

        :return: True if the SDK is available, False if not, None if platform is not Android.
        """


        platform = self.page.platform.value

        if platform != 'android':
            return None

        result = self.invoke_method_async(
            method_name="get_health_connect_sdk_status",
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        if result == 'HealthConnectSdkStatus.sdkAvailable':
            return True
        else:
            return False

    def get_total_steps_in_interval(
            self,
            start_time: datetime,
            end_time: datetime,
            include_manual_entry: Optional[bool] = True,
            wait_timeout: Optional[float] = 25
    ):
        """
        Get the total number of steps within a specific time period.

        :return: `None` if not successful
        """

        start_time_ms = int(start_time.timestamp() * 1000)
        end_time_ms = int(end_time.timestamp() * 1000)

        data = json.dumps(
            {
                "start_time": start_time_ms,
                "end_time": end_time_ms,
                "include_manual_entry": include_manual_entry
            }
        )

        result = self.invoke_method(
            method_name="get_total_steps_in_interval",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return int(result) if result else None

    async def get_total_steps_in_interval_async(
            self,
            start_time: datetime,
            end_time: datetime,
            include_manual_entry: Optional[bool] = True,
            wait_timeout: Optional[float] = 25
    ):
        """
        Get the total number of steps within a specific time period.

        :return: `None` if not successful
        """

        start_time_ms = int(start_time.timestamp() * 1000)
        end_time_ms = int(end_time.timestamp() * 1000)

        data = json.dumps(
            {
                "start_time": start_time_ms,
                "end_time": end_time_ms,
                "include_manual_entry": include_manual_entry
            }
        )

        result = await self.invoke_method_async(
            method_name="get_total_steps_in_interval",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return int(result) if result else None

    def get_health_aggregate_data_from_types(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: datetime,
            activity_segment_duration: Optional[int] = 1,
            include_manual_entry: Optional[bool] = True,
            wait_timeout: Optional[float] = 25
    ):
        """
        Fetch a list of health data points based on [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType]
        """

        # Validate types
        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        # Convert types to their string values
        types_str = [t.value for t in types]
        start_time_ms = int(start_time.timestamp() * 1000)
        end_time_ms = int(end_time.timestamp() * 1000)

        data = json.dumps(
            {
                "types": types_str,
                "start_time": start_time_ms,
                "end_time": end_time_ms,
                "activity_segment_duration": activity_segment_duration,
                "include_manual_entry": include_manual_entry
            }
        )

        result = self.invoke_method(
            method_name="get_health_aggregate_data_from_types",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return json.loads(result) if result else []

    async def get_health_aggregate_data_from_types_async(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: datetime,
            activity_segment_duration: Optional[int] = 1,
            include_manual_entry: Optional[bool] = True,
            wait_timeout: Optional[float] = 25
    ):
        """
        Fetch a list of health data points based on [HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType]
        """

        # Validate types
        if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
            raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

        # Convert types to their string values
        types_str = [t.value for t in types]
        start_time_ms = int(start_time.timestamp() * 1000)
        end_time_ms = int(end_time.timestamp() * 1000)

        data = json.dumps(
            {
                "types": types_str,
                "start_time": start_time_ms,
                "end_time": end_time_ms,
                "activity_segment_duration": activity_segment_duration,
                "include_manual_entry": include_manual_entry
            }
        )

        result = await self.invoke_method_async(
            method_name="get_health_aggregate_data_from_types",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return json.loads(result) if result else []

    def get_health_data_from_types(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: datetime,
            recording_method: Optional[List[RecordingMethod]] = None,
            wait_timeout: Optional[float] = 25
    ) -> str | list[Any] | None:
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

            # Validate recording methods
            if recording_method and not all(isinstance(rc, RecordingMethod) for rc in recording_method):
                raise ValueError("The 'recording_method' argument must be an instance of 'RecordingMethod'.")

            # Validate types
            if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
                raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

            # Convert types to their string values
            types_str = [t.value for t in types]

            # Convert datetimes to milliseconds since epoch
            start_time_ms = int(start_time.timestamp() * 1000)
            end_time_ms = int(end_time.timestamp() * 1000)

            # Prepare arguments for the invoke_method call
            data = json.dumps(
                {
                    "types": types_str,
                    "start_time": start_time_ms,
                    "end_time": end_time_ms,
                    "recording_method": [rm.value for rm in recording_method] if recording_method else [],
                }
            )

            # Call the native method
            result = self.invoke_method(
                method_name="get_health_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            return json.loads(result) if result else []

        except Exception as error:
            print(f"Error in get_health_data_from_types: {error}")
            return []

    async def get_health_data_from_types_async(
            self,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: datetime,
            recording_method: Optional[List[RecordingMethod]] = None,
            wait_timeout: Optional[float] = 25
    ) -> str | list[Any] | None:
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

            # Validate recording methods
            if recording_method and not all(isinstance(rc, RecordingMethod) for rc in recording_method):
                raise ValueError("The 'recording_method' argument must be an instance of 'RecordingMethod'.")

            # Validate types
            if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
                raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

            # Convert types to their string values
            types_str = [t.value for t in types]

            # Convert datetimes to milliseconds since epoch
            start_time_ms = int(start_time.timestamp() * 1000)
            end_time_ms = int(end_time.timestamp() * 1000)

            # Prepare arguments for the invoke_method call
            data = json.dumps(
                {
                    "types": types_str,
                    "start_time": start_time_ms,
                    "end_time": end_time_ms,
                    "recording_method": [rm.value for rm in recording_method] if recording_method else [],
                }
            )

            # Call the native method
            result = await self.invoke_method_async(
                method_name="get_health_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            return json.loads(result) if result else []

        except Exception as error:
            print(f"Error in get_health_data_from_types: {error}")
            return []

    def get_health_interval_data_from_types(
            self,
            start_time: datetime,
            end_time: datetime,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            interval: int,
            recording_method: Optional[List[RecordingMethod]] = None,
            wait_timeout: Optional[float] = 25
    ) -> list[Any]:
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

            # Validate recording methods
            if recording_method and not all(isinstance(rc, RecordingMethod) for rc in recording_method):
                raise ValueError("The 'recording_method' argument must be an instance of 'RecordingMethod'.")

            # Validate types
            if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
                raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

            # Convert types to their string values
            types_str = [t.value for t in types]

            # Convert datetimes to milliseconds since epoch
            start_time_ms = int(start_time.timestamp() * 1000)
            end_time_ms = int(end_time.timestamp() * 1000)

            # Prepare arguments for the invoke_method call
            data = json.dumps(
                {
                    "start_time": start_time_ms,
                    "end_time": end_time_ms,
                    "types": types_str,
                    "interval": interval,
                    "recording_method": [rm.value for rm in recording_method] if recording_method else [],
                }
            )

            # Call the native method
            result = self.invoke_method(
                method_name="get_health_interval_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            return json.loads(result) if result else []

        except Exception as e:
            print(f"Error in get_health_interval_data_from_types: {e}")
            return []

    async def get_health_interval_data_from_types_async(
            self,
            start_time: datetime,
            end_time: datetime,
            types: List[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            interval: int,
            recording_method: Optional[List[RecordingMethod]] = None,
            wait_timeout: Optional[float] = 25
    ) -> list[Any]:
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

            # Validate recording methods
            if recording_method and not all(isinstance(rc, RecordingMethod) for rc in recording_method):
                raise ValueError("The 'recording_method' argument must be an instance of 'RecordingMethod'.")

            # Validate types
            if not all(isinstance(t, HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType) for t in types):
                raise ValueError("All elements of 'types' must be instances of 'HealthDataTypeAndroid, HealthDataTypeIOS or HealthWorkoutActivityType'.")

            # Convert types to their string values
            types_str = [t.value for t in types]

            # Convert datetimes to milliseconds since epoch
            start_time_ms = int(start_time.timestamp() * 1000)
            end_time_ms = int(end_time.timestamp() * 1000)

            # Prepare arguments for the invoke_method call
            data = json.dumps(
                {
                    "start_time": start_time_ms,
                    "end_time": end_time_ms,
                    "types": types_str,
                    "interval": interval,
                    "recording_method": [rm.value for rm in recording_method] if recording_method else [],
                }
            )

            # Call the native method
            result = await self.invoke_method_async(
                method_name="get_health_interval_data_from_types",
                arguments={'data': data},
                wait_for_result=True,
                wait_timeout=wait_timeout
            )

            return json.loads(result) if result else []

        except Exception as e:
            print(f"Error in get_health_interval_data_from_types: {e}")
            return []

    def write_blood_oxygen(
            self,
            saturation: float,
            start_time: datetime,
            end_time: datetime,
            recording_method: Optional[RecordingMethod] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves blood oxygen saturation record.

        :return: True if successful, False otherwise
        """

        # Validate recording methods
        if recording_method and not isinstance(recording_method, RecordingMethod):
            raise ValueError(f"Invalid recording method: {recording_method}.")

        data = json.dumps(
            {
                "saturation": saturation,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "recording_method": recording_method.value,
            }
        )

        result = self.invoke_method(
            method_name="write_blood_oxygen",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    async def write_blood_oxygen_async(
            self,
            saturation: float,
            start_time: datetime,
            end_time: datetime,
            recording_method: Optional[RecordingMethod] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves blood oxygen saturation record.

        :return: True if successful, False otherwise
        """

        # Validate recording methods
        if recording_method and not isinstance(recording_method, RecordingMethod):
            raise ValueError(f"Invalid recording method: {recording_method}.")

        data = json.dumps(
            {
                "saturation": saturation,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "recording_method": recording_method.value,
            }
        )

        result = await self.invoke_method_async(
            method_name="write_blood_oxygen",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    def write_health_data(
            self,
            value: float,
            start_time: datetime,
            end_time: datetime,
            types: HealthDataTypeAndroid | HealthDataTypeIOS,
            unit: Optional[HealthDataUnit] = None,
            recording_method: Optional[RecordingMethod] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
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

        data = json.dumps(
            {
                "value": value,
                "types": types.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "unit": unit.value if unit else HealthDataUnit.NO_UNIT.value,
                "recording_method": recording_method.value if recording_method else RecordingMethod.AUTOMATIC.value
            }
        )

        result = self.invoke_method(
            method_name="write_health_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def write_health_data_async(
            self,
            value: float,
            start_time: datetime,
            end_time: datetime,
            types: HealthDataTypeAndroid | HealthDataTypeIOS,
            unit: Optional[HealthDataUnit] = None,
            recording_method: Optional[RecordingMethod] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
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

        data = json.dumps(
            {
                "value": value,
                "types": types.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "unit": unit.value if unit else HealthDataUnit.NO_UNIT.value,
                "recording_method": recording_method.value if recording_method else RecordingMethod.AUTOMATIC.value
            }
        )

        result = await self.invoke_method_async(
            method_name="write_health_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    def write_workout_data(
            self,
            activity_type: HealthWorkoutActivityType,
            start_time: datetime,
            end_time: datetime,
            total_energy_burned: Optional[int] = None,
            total_energy_burned_unit: Optional[HealthDataUnit] = None,
            total_distance: Optional[int] = None,
            total_distance_unit: Optional[HealthDataUnit] = None,
            title: Optional[str] = None,
            recording_method: Optional[RecordingMethod] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Write workout data to Apple Health or Google Health Connect.

        :return: True if the workout data was successfully added.
        """

        data = json.dumps(
            {
                "activity_type": activity_type.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "total_energy_burned": total_energy_burned,
                "total_energy_burned_unit": total_energy_burned_unit.value if total_energy_burned_unit else HealthDataUnit.KILOCALORIE.value,
                "total_distance": total_distance,
                "total_distance_unit": total_distance_unit.value if total_distance_unit else HealthDataUnit.METER.value,
                "title": title,
                "recording_method": recording_method.value if recording_method else RecordingMethod.AUTOMATIC.value,
            }
        )
        result = self.invoke_method(
            method_name="write_workout_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    async def write_workout_data_async(
            self,
            activity_type: HealthWorkoutActivityType,
            start_time: datetime,
            end_time: datetime,
            total_energy_burned: Optional[int] = None,
            total_energy_burned_unit: Optional[HealthDataUnit] = None,
            total_distance: Optional[int] = None,
            total_distance_unit: Optional[HealthDataUnit] = None,
            title: Optional[str] = None,
            recording_method: Optional[RecordingMethod] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Write workout data to Apple Health or Google Health Connect.

        :return: True if the workout data was successfully added.
        """

        data = json.dumps(
            {
                "activity_type": activity_type.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "total_energy_burned": total_energy_burned,
                "total_energy_burned_unit": total_energy_burned_unit.value if total_energy_burned_unit else HealthDataUnit.KILOCALORIE.value,
                "total_distance": total_distance,
                "total_distance_unit": total_distance_unit.value if total_distance_unit else HealthDataUnit.METER.value,
                "title": title,
                "recording_method": recording_method.value if recording_method else RecordingMethod.AUTOMATIC.value,
            }
        )
        result = await self.invoke_method_async(
            method_name="write_workout_data",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    def write_blood_pressure(
            self,
            systolic: int,
            diastolic: int,
            start_time: datetime,
            recording_method: Optional[RecordingMethod] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves a blood pressure record.

        :return: True if successful, false otherwise.
        """

        data = json.dumps(
            {
                "systolic": systolic,
                "diastolic": diastolic,
                "start_time": int(start_time.timestamp() * 1000),
                "recording_method": recording_method if recording_method else None,
            }
        )

        result = self.invoke_method(
            method_name="write_blood_pressure",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    async def write_blood_pressure_async(
            self,
            systolic: int,
            diastolic: int,
            start_time: datetime,
            recording_method: Optional[RecordingMethod] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves a blood pressure record.

        :return: True if successful, false otherwise.
        """

        data = json.dumps(
            {
                "systolic": systolic,
                "diastolic": diastolic,
                "start_time": int(start_time.timestamp() * 1000),
                "recording_method": recording_method if recording_method else None,
            }
        )

        result = await self.invoke_method_async(
            method_name="write_blood_pressure",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    def write_meal(
            self,
            meal_type: MealType,
            start_time: datetime,
            end_time: datetime,
            calories_consumed: Optional[float] = None,
            carbohydrates: Optional[float] = None,
            protein: Optional[float] = None,
            fat_total: Optional[float] = None,
            name: Optional[str] = None,
            caffeine: Optional[float] = None,
            vitamin_a: Optional[float] = None,
            b1_thiamin: Optional[float] = None,
            b2_riboflavin: Optional[float] = None,
            b3_niacin: Optional[float] = None,
            b5_pantothenic_acid: Optional[float] = None,
            b6_pyridoxine: Optional[float] = None,
            b7_biotin: Optional[float] = None,
            b9_folate: Optional[float] = None,
            b12_cobalamin: Optional[float] = None,
            vitamin_c: Optional[float] = None,
            vitamin_d: Optional[float] = None,
            vitamin_e: Optional[float] = None,
            vitamin_k: Optional[float] = None,
            calcium: Optional[float] = None,
            cholesterol: Optional[float] = None,
            chloride: Optional[float] = None,
            chromium: Optional[float] = None,
            copper: Optional[float] = None,
            fat_unsaturated: Optional[float] = None,
            fat_monounsaturated: Optional[float] = None,
            fat_polyunsaturated: Optional[float] = None,
            fat_saturated: Optional[float] = None,
            fat_trans_monoenoic: Optional[float] = None,
            fiber: Optional[float] = None,
            iodine: Optional[float] = None,
            iron: Optional[float] = None,
            magnesium: Optional[float] = None,
            manganese: Optional[float] = None,
            molybdenum: Optional[float] = None,
            phosphorus: Optional[float] = None,
            potassium: Optional[float] = None,
            selenium: Optional[float] = None,
            sodium: Optional[float] = None,
            sugar: Optional[float] = None,
            water: Optional[float] = None,
            zinc: Optional[float] = None,
            recording_method: Optional[str] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves meal record into Apple Health or Health Connect.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "meal_type": meal_type.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "calories_consumed": calories_consumed,
                "carbohydrates": carbohydrates,
                "protein": protein,
                "fat_total": fat_total,
                "name": name,
                "caffeine": caffeine,
                "vitamin_a": vitamin_a,
                "b1_thiamin": b1_thiamin,
                "b2_riboflavin": b2_riboflavin,
                "b3_niacin": b3_niacin,
                "b5_pantothenic_acid": b5_pantothenic_acid,
                "b6_pyridoxine": b6_pyridoxine,
                "b7_biotin": b7_biotin,
                "b9_folate": b9_folate,
                "b12_cobalamin": b12_cobalamin,
                "vitamin_c": vitamin_c,
                "vitamin_d": vitamin_d,
                "vitamin_e": vitamin_e,
                "vitamin_k": vitamin_k,
                "calcium": calcium,
                "cholesterol": cholesterol,
                "chloride": chloride,
                "chromium": chromium,
                "copper": copper,
                "fat_unsaturated": fat_unsaturated,
                "fat_monounsaturated": fat_monounsaturated,
                "fat_polyunsaturated": fat_polyunsaturated,
                "fat_saturated": fat_saturated,
                "fat_trans_monoenoic": fat_trans_monoenoic,
                "fiber": fiber,
                "iodine": iodine,
                "iron": iron,
                "magnesium": magnesium,
                "manganese": manganese,
                "molybdenum": molybdenum,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "selenium": selenium,
                "sodium": sodium,
                "sugar": sugar,
                "water": water,
                "zinc": zinc,
                "recording_method": recording_method,
            }
        )

        result = self.invoke_method(
            method_name="write_meal",  # The key name for the flutter case
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def write_meal_async(
            self,
            meal_type: MealType,
            start_time: datetime,
            end_time: datetime,
            calories_consumed: Optional[float] = None,
            carbohydrates: Optional[float] = None,
            protein: Optional[float] = None,
            fat_total: Optional[float] = None,
            name: Optional[str] = None,
            caffeine: Optional[float] = None,
            vitamin_a: Optional[float] = None,
            b1_thiamin: Optional[float] = None,
            b2_riboflavin: Optional[float] = None,
            b3_niacin: Optional[float] = None,
            b5_pantothenic_acid: Optional[float] = None,
            b6_pyridoxine: Optional[float] = None,
            b7_biotin: Optional[float] = None,
            b9_folate: Optional[float] = None,
            b12_cobalamin: Optional[float] = None,
            vitamin_c: Optional[float] = None,
            vitamin_d: Optional[float] = None,
            vitamin_e: Optional[float] = None,
            vitamin_k: Optional[float] = None,
            calcium: Optional[float] = None,
            cholesterol: Optional[float] = None,
            chloride: Optional[float] = None,
            chromium: Optional[float] = None,
            copper: Optional[float] = None,
            fat_unsaturated: Optional[float] = None,
            fat_monounsaturated: Optional[float] = None,
            fat_polyunsaturated: Optional[float] = None,
            fat_saturated: Optional[float] = None,
            fat_trans_monoenoic: Optional[float] = None,
            fiber: Optional[float] = None,
            iodine: Optional[float] = None,
            iron: Optional[float] = None,
            magnesium: Optional[float] = None,
            manganese: Optional[float] = None,
            molybdenum: Optional[float] = None,
            phosphorus: Optional[float] = None,
            potassium: Optional[float] = None,
            selenium: Optional[float] = None,
            sodium: Optional[float] = None,
            sugar: Optional[float] = None,
            water: Optional[float] = None,
            zinc: Optional[float] = None,
            recording_method: Optional[str] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves meal record into Apple Health or Health Connect.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "meal_type": meal_type.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "calories_consumed": calories_consumed,
                "carbohydrates": carbohydrates,
                "protein": protein,
                "fat_total": fat_total,
                "name": name,
                "caffeine": caffeine,
                "vitamin_a": vitamin_a,
                "b1_thiamin": b1_thiamin,
                "b2_riboflavin": b2_riboflavin,
                "b3_niacin": b3_niacin,
                "b5_pantothenic_acid": b5_pantothenic_acid,
                "b6_pyridoxine": b6_pyridoxine,
                "b7_biotin": b7_biotin,
                "b9_folate": b9_folate,
                "b12_cobalamin": b12_cobalamin,
                "vitamin_c": vitamin_c,
                "vitamin_d": vitamin_d,
                "vitamin_e": vitamin_e,
                "vitamin_k": vitamin_k,
                "calcium": calcium,
                "cholesterol": cholesterol,
                "chloride": chloride,
                "chromium": chromium,
                "copper": copper,
                "fat_unsaturated": fat_unsaturated,
                "fat_monounsaturated": fat_monounsaturated,
                "fat_polyunsaturated": fat_polyunsaturated,
                "fat_saturated": fat_saturated,
                "fat_trans_monoenoic": fat_trans_monoenoic,
                "fiber": fiber,
                "iodine": iodine,
                "iron": iron,
                "magnesium": magnesium,
                "manganese": manganese,
                "molybdenum": molybdenum,
                "phosphorus": phosphorus,
                "potassium": potassium,
                "selenium": selenium,
                "sodium": sodium,
                "sugar": sugar,
                "water": water,
                "zinc": zinc,
                "recording_method": recording_method,
            }
        )

        result = await self.invoke_method_async(
            method_name="write_meal",  # The key name for the flutter case
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    def write_audiogram(
            self,
            frequencies: List[float],
            left_ear_sensitivities: List[float],
            right_ear_sensitivities: List[float],
            start_time: datetime,
            end_time: datetime,
            metadata: Optional[Dict[str, Any]] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves audiogram into Apple Health. Not supported on Android.

        :return: True if successful, false otherwise.
        """

        platform = self.page.platform.value

        if platform == 'android':
            raise ValueError('writeAudiogram is not supported on Android')

        data = json.dumps(
            {
                "frequencies": frequencies,
                "left_ear_sensitivities": left_ear_sensitivities,
                "right_ear_sensitivities": right_ear_sensitivities,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "metadata": metadata,
            }
        )

        result = self.invoke_method(
            method_name="write_audiogram",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    async def write_audiogram_async(
            self,
            frequencies: List[float],
            left_ear_sensitivities: List[float],
            right_ear_sensitivities: List[float],
            start_time: datetime,
            end_time: datetime,
            metadata: Optional[Dict[str, Any]] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Saves audiogram into Apple Health. Not supported on Android.

        :return: True if successful, false otherwise.
        """

        platform = self.page.platform.value

        if platform == 'android':
            raise ValueError('writeAudiogram is not supported on Android')

        data = json.dumps(
            {
                "frequencies": frequencies,
                "left_ear_sensitivities": left_ear_sensitivities,
                "right_ear_sensitivities": right_ear_sensitivities,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "metadata": metadata,
            }
        )

        result = await self.invoke_method_async(
            method_name="write_audiogram",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    def write_menstruation_flow(
            self,
            flow: MenstrualFlow,
            start_time: datetime,
            end_time: datetime,
            is_start_of_cycle: bool,
            recording_method: Optional[str] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Save menstruation flow into Apple Health and Google Health Connect.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "flow": flow.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "is_start_of_cycle": is_start_of_cycle,
                "recording_method": recording_method if recording_method else None,
            }
        )

        result = self.invoke_method(
            method_name="write_menstruation_flow",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    async def write_menstruation_flow_async(
            self,
            flow: MenstrualFlow,
            start_time: datetime,
            end_time: datetime,
            is_start_of_cycle: bool,
            recording_method: Optional[str] = RecordingMethod.AUTOMATIC,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Save menstruation flow into Apple Health and Google Health Connect.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "flow": flow.value,
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000),
                "is_start_of_cycle": is_start_of_cycle,
                "recording_method": recording_method if recording_method else None,
            }
        )

        result = await self.invoke_method_async(
            method_name="write_menstruation_flow",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )
        return result == "true"

    def write_insulin_delivery(
            self,
            units: float,
            reason: InsulinDeliveryReason,
            start_time: datetime,
            end_time: datetime,
            wait_timeout: float = 25
    ):
        """
        Saves insulin delivery record into Apple Health.

        :return: True if successful, False otherwise.
        """

        data = json.dumps({
            "units": units,
            "reason": reason,
            "start_time": int(start_time.timestamp() * 1000),
            "end_time": int(end_time.timestamp() * 1000),
        })

        result = self.invoke_method(
            method_name="write_insulin_delivery",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def write_insulin_delivery_async(
            self,
            units: float,
            reason: InsulinDeliveryReason,
            start_time: datetime,
            end_time: datetime,
            wait_timeout: float = 25
    ):
        """
        No description.
        """

        data = json.dumps({
            "units": units,
            "reason": reason,
            "start_time": int(start_time.timestamp() * 1000),
            "end_time": int(end_time.timestamp() * 1000),
        })

        result = await self.invoke_method_async(
            method_name="write_insulin_delivery",
            arguments={"data": data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"


    def delete(
            self,
            types: Optional[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: Optional[datetime] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Deletes all records of the given [type] for a given period of time.

        :param types: - the value's HealthDataType.
        :param start_time: - the start time when this [value] is measured. Must be equal to or earlier than [endTime].
        :param end_time: - the end time when this [value] is measured. Must be equal to or later than [startTime].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "types": types.value if types else "",
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000) if end_time else None
            }
        )

        result = self.invoke_method(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def delete_async(
            self,
            types: Optional[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType],
            start_time: datetime,
            end_time: Optional[datetime] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Deletes all records of the given [type] for a given period of time.

        :param types: - the value's HealthDataType.
        :param start_time: - the start time when this [value] is measured. Must be equal to or earlier than [endTime].
        :param end_time: - the end time when this [value] is measured. Must be equal to or later than [startTime].
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "types": types.value if types else "",
                "start_time": int(start_time.timestamp() * 1000),
                "end_time": int(end_time.timestamp() * 1000) if end_time else None
            }
        )

        result = await self.invoke_method_async(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    def delete_by_uuid(
            self,
            uuid: str,
            types: Optional[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Deletes a specific health record by its UUID.

        :param uuid: - The UUID of the health record to delete.
        :param types: - The health data type of the record. Required on iOS.
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        On Android, only the UUID is required. On iOS, both UUID and type are required.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "uuid": uuid,
                "types": types.value if types else ""
            }
        )

        result = self.invoke_method(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    async def delete_by_uuid_async(
            self,
            uuid: str,
            types: Optional[HealthDataTypeAndroid | HealthDataTypeIOS | HealthWorkoutActivityType] = None,
            wait_timeout: Optional[float] = 25
    ) -> bool:
        """
        Deletes a specific health record by its UUID.

        :param uuid: - The UUID of the health record to delete.
        :param types: - The health data type of the record. Required on iOS.
        :param wait_timeout: The maximum time to wait for the method to complete. Defaults to 25 seconds.

        On Android, only the UUID is required. On iOS, both UUID and type are required.

        :return: True if successful, False otherwise.
        """

        data = json.dumps(
            {
                "uuid": uuid,
                "types": types.value if types else ""
            }
        )

        result = await self.invoke_method_async(
            method_name="delete_by_uuid",
            arguments={'data': data},
            wait_for_result=True,
            wait_timeout=wait_timeout
        )

        return result == "true"

    @property
    def on_error(self) -> OptionalControlEventCallable:
        return self._get_attr("error")

    @on_error.setter
    def on_error(self, handler: OptionalControlEventCallable):
        self._add_event_handler("error", handler)
