import os
import re
import asyncio
import logging
import contextlib
import flet as ft
import flet_health as fh
from enum import Enum
from functools import partial
from datetime import datetime, timedelta


log_file_path = os.getenv("FLET_APP_CONSOLE") or "debug.log"

logging.basicConfig(
    level=logging.INFO,
    format="[{asctime}] [{levelname}] [{filename}:{funcName}:{lineno}] - {message}",
    style="{",
    handlers=[
        logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
    ]
)

logger = logging.getLogger(__name__)


def parse_log_block(lines: list[str]) -> list[dict]:
    logs = []
    buffer = []

    for line in lines:
        if re.match(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+] \[.*?]", line):
            if buffer:
                logs.append("".join(buffer))
                buffer.clear()
        buffer.append(line)
    if buffer:
        logs.append("".join(buffer))

    parsed_logs = []
    for entry in logs:
        match = re.search(r"\[(.*?)] \[(.*?)] \[(.*?):(.*?):(\d+)] - (.+)", entry, re.DOTALL)
        if match:
            timestamp, level, file, func, line_no, message = match.groups()
            parsed_logs.append({
                "timestamp": timestamp,
                "level": level,
                "file": file,
                "func": func,
                "line": line_no,
                "message": message.strip()
            })
    return parsed_logs


def color_for_level(level: str):
    return {
        "INFO": ft.Colors.BLUE_100,
        "WARNING": ft.Colors.AMBER_100,
        "ERROR": ft.Colors.RED_100,
        "DEBUG": ft.Colors.GREY_100
    }.get(level, ft.Colors.GREY_200)


def show_console_log(e: ft.ControlEvent) -> None:
    if not log_file_path or not os.path.exists(log_file_path):
        open_snack_bar(e.page, "No logs found")
        return

    with open(log_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    parsed_logs = parse_log_block(lines)

    log_controls = []
    for log in parsed_logs:

        # Formatar data
        formatted_timestamp = log["timestamp"]
        with contextlib.suppress(Exception):
            dt_obj = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S,%f")
            formatted_timestamp = dt_obj.strftime("%d/%m/%Y | %H:%M:%S")

        log_controls.append(
            ft.Container(
                bgcolor=color_for_level(log["level"]),
                border_radius=10,
                padding=10,
                margin=5,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Text(f"📄 {log['file']} | line: {log['line']} | func: {log['func']}", weight=ft.FontWeight.BOLD, size=10, selectable=True),
                        ft.Text(f"⏱️ {formatted_timestamp}", size=10, italic=True, selectable=True),
                        ft.Text(f"📌 messgage:", size=10, italic=True),
                        ft.Text(
                            f"{log['message']}",
                            size=10,
                            selectable=True,
                            max_lines=15 if len(log['message']) > 100 else None,
                            overflow=ft.TextOverflow.VISIBLE
                        ),
                    ]
                )
            )
        )

    dialog = ft.AlertDialog(
        title=ft.Text("Debug Logs"),
        content=ft.Container(
            height=500,
            width=380,
            content=ft.ListView(controls=log_controls, auto_scroll=True)
        ),
        scrollable=True
    )

    e.page.open(dialog)
    e.page.debug_icon.clear_notify(e.page)


class SnackBarType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    NONE = "none"


def open_snack_bar(page: ft.Page, msg, snack_type: SnackBarType = SnackBarType.NONE, duration=3000):
    """Opens a SnackBar with a message and type-based styling."""

    snackbar = getattr(page, 'snackbar')

    match snack_type.value:
        case 'info':
            bgcolor = ft.Colors.BLUE_100
            text_colors = ft.Colors.BLUE_900
        case 'success':
            bgcolor = ft.Colors.GREEN_ACCENT_100
            text_colors = ft.Colors.GREEN_900
        case 'warning':
            bgcolor = ft.Colors.AMBER_100
            text_colors = ft.Colors.AMBER_900
        case 'error':
            bgcolor = ft.Colors.RED_ACCENT_100
            text_colors = ft.Colors.RED_900
        case 'none':
            bgcolor = ft.Colors.BLACK87
            text_colors = ft.Colors.WHITE
        case _:
            bgcolor = ft.Colors.BLACK87
            text_colors = ft.Colors.WHITE

    # Atualiza o conteúdo e estilo
    snackbar.content = ft.Text(msg, color=text_colors)
    snackbar.bgcolor = bgcolor
    snackbar.duration = duration

    # Exibe o snackbar
    page.open(snackbar)


class DebugNotificationIcon(ft.Stack):
    def __init__(self, page, func):
        super().__init__()
        self.page = page
        self.func = func
        self.number_errors = 0
        self.debug_button = ft.IconButton(
            icon=ft.Icons.BUG_REPORT,
            tooltip="Show logs",
            padding=ft.padding.only(right=20),
            on_click=self.func,
        )

        self.text_notifi = ft.Text(
            color=ft.Colors.WHITE,
            size=10,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        self.container = ft.Container(
            margin=ft.margin.only(top=20),
            bgcolor=ft.Colors.RED,
            border_radius=10,
            width=20,
            height=20,
            alignment=ft.alignment.center,
            offset=ft.Offset(0.5, -0.5),
            # on_click=self.func,
        )

    def add_notify_error(self, page: ft.Page):
        self.number_errors += 1
        self.text_notifi.value = (
            str(self.number_errors) if self.number_errors < 11 else '. . .'
        )
        self.container.content = self.text_notifi
        self.container.bgcolor = ft.Colors.RED
        self.controls.append(self.container)
        page.update()

    def clear_notify(self, page: ft.Page):
        self.number_errors = 0
        self.container.content = None
        self.container.bgcolor = None
        page.update()

    def build(self):
        self.controls = [self.debug_button]
        if self.number_errors > 0:
            self.controls.append(self.container)


class StartupPage(ft.View):
    def __init__(self, page: ft.Page, health: fh.Health):
        super().__init__(route="/startup", controls=[])
        self.page = page
        self.health = health
        self.debug_icon = getattr(self.page, 'debug_icon')
        self.appbar = self.page.appbar
        self.status_text = ft.Text("Checking the Health Connect SDK...")
        self.install_button = ft.ElevatedButton(
            text="Install Health Connect",
            visible=False,
            on_click=lambda _: self.health.install_health_connect()
        )

        self.progress_ring = ft.ProgressRing(
            width=15,
            height=15,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.BLUE_400,
            visible=True,
        )
        self.progress_ring_container = ft.Container(
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ]
            )
        )
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Text("Welcome to Flet Health!"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    self.status_text,
                                    self.progress_ring_container
                                ]
                            ),
                            self.install_button,
                        ]
                    )
                ]
            )
        ]

    def did_mount(self):
        logger.info("did_mount")
        self.page.run_task(self.check_health_connect)

    def will_unmount(self):
        logger.info("will_unmount")

    async def check_health_connect(self):
        try:
            self.install_button.visible = False
            self.install_button.update()
            self.status_text.value = "Checking the Health Connect SDK..."
            self.status_text.update()
            self.progress_ring_container.content.controls[0].controls.append(self.progress_ring)
            self.progress_ring.visible = True
            self.progress_ring_container.update()
            await asyncio.sleep(1)
            status =  await self.health.get_health_connect_sdk_status_async()
            logger.info(f"SDK status: {status}")

            if status == fh.HealthConnectSdkStatus.SDK_AVAILABLE or status is None:
                self.install_button.visible = False
                self.page.go("/")
            else:
                self.status_text.value = "Health Connect is not installed on this device."
                self.install_button.visible = True

        except Exception as error:
            self.status_text.value = None
            logger.error(f"Error checking Health Connect SDK status", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page, f"Error checking Health Connect SDK status: {error}", SnackBarType.ERROR)

        finally:
            self.progress_ring.visible = False
            self.progress_ring_container.content.controls[0].controls.remove(self.progress_ring)
            self.page.update()


class SessionsPage(ft.View):
    def __init__(self, page: ft.Page, health: fh.Health):
        super().__init__()
        self.page = page
        self.health = health
        self.debug_icon = getattr(self.page, 'debug_icon')
        self.health.on_error = self.handle_error
        self.appbar = self.page.appbar
        self.drawer = self.page.drawer
        self.end_time = datetime.now()
        self.start_time = self.end_time - timedelta(days=1)
        self.has_permissions = False

        self.list_view = ft.ListView(
            divider_thickness=1,
            expand=True,
            auto_scroll=True,
            spacing=5,
        )

        self.data_result_list = ft.Container(
            width=self.page.width,
            height=300,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_300,
            padding=ft.padding.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.list_view
                ]
            )
        )

        self.controls = [
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Request Permissions",
                                on_click=self.request_permissions
                            ),
                        ]
                    ),
                ]
            )
        ]

    def did_mount(self):
        logger.info("did_mount")
        self.page.run_task(self.check_permission)

    def will_unmount(self):
        logger.info("will_unmount")

    def build(self):
        logger.info("build")
        return ft.Column(controls=self.controls)

    async def check_permission(self):
        try:
            self.has_permissions = await self.health.has_permissions_async(
                types=[
                    fh.HealthDataTypeAndroid.STEPS,
                    fh.HealthDataTypeAndroid.DISTANCE_DELTA,
                    fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
                ],
                data_access=[
                    fh.DataAccess.READ_WRITE,
                    fh.DataAccess.READ_WRITE,
                    fh.DataAccess.READ_WRITE
                ]
            )
        except Exception as error:
            logger.error(f"Error checking permissions", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page,f"Error checking permissions: {error}", SnackBarType.ERROR)

        await self.update_controls()

    async def update_controls(self):
        if self.has_permissions:
            self.controls = [
                ft.Row(
                    wrap=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Start Time"),
                                ft.Row(
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        start_date_field := ft.TextField(
                                            width=150,
                                            label="Date",
                                            prefix_icon=ft.Icons.DATE_RANGE,
                                            value=(datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y"),
                                            read_only=True,
                                            on_click=lambda e: self.page.open(
                                                ft.DatePicker(
                                                    value=datetime.now() - timedelta(days=1),
                                                    first_date=datetime(year=2000, month=10, day=1),
                                                    last_date=datetime(year=2025, month=10, day=1),
                                                    on_change=partial(self.handle_date_change, start_date_field=start_date_field),
                                                    on_dismiss=self.handle_dismissal,
                                                )
                                            ),
                                        ),
                                        start_time_field := ft.TextField(
                                            width=150,
                                            label="Time",
                                            prefix_icon=ft.Icons.TIMER_OUTLINED,
                                            value=datetime.now().strftime("%H:%M"),
                                            read_only=True,
                                            data="start_time",
                                            on_click=lambda e: self.page.open(
                                                ft.TimePicker(
                                                    value=datetime.now().time(),
                                                    confirm_text="Confirm",
                                                    error_invalid_text="Time out of range",
                                                    help_text="Pick your time slot",
                                                    on_change=partial(self.handle_time_change, start_time_field=start_time_field),
                                                    on_dismiss=self.handle_dismissal,
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                                ft.Text("End Time"),
                                ft.Row(
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        end_date_field := ft.TextField(
                                            width=150,
                                            label="Date",
                                            prefix_icon=ft.Icons.DATE_RANGE,
                                            value=datetime.now().strftime("%d/%m/%Y"),
                                            read_only=True,
                                            on_click=lambda e: self.page.open(
                                                ft.DatePicker(
                                                    first_date=datetime(year=2000, month=10, day=1),
                                                    last_date=datetime(year=2025, month=10, day=1),
                                                    on_change=partial(self.handle_date_change, end_date_field=end_date_field),
                                                    on_dismiss=self.handle_dismissal,
                                                )
                                            ),
                                        ),
                                        end_time_field := ft.TextField(
                                            width=150,
                                            label="Time",
                                            prefix_icon=ft.Icons.TIMER_OUTLINED,
                                            value=datetime.now().strftime("%H:%M"),
                                            read_only=True,
                                            data="start_time",
                                            on_click=lambda e: self.page.open(
                                                ft.TimePicker(
                                                    confirm_text="Confirm",
                                                    error_invalid_text="Time out of range",
                                                    help_text="Pick your time slot",
                                                    on_change=partial(self.handle_time_change, end_time_field=end_time_field),
                                                    on_dismiss=self.handle_dismissal,
                                                )
                                            ),
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        ft.ElevatedButton("Insert Data", on_click=self.insert_health_data),
                                        ft.ElevatedButton("Read Data", on_click=self.read_health_data),
                                        ft.ElevatedButton("Background Read", on_click=self.request_background_read),
                                    ]
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.GREY_300,
                                    width=self.page.width,
                                    height=3,
                                ),
                                ft.Column(
                                    scroll=ft.ScrollMode.ALWAYS,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Health Data"),
                                        self.data_result_list,
                                    ]
                                )
                            ]
                        ),
                    ]
                )
            ]
        else:
            self.controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton("Request Permissions", on_click=self.request_permissions),
                            ]
                        ),
                    ]
                )
            ]

        self.page.update()

    async def request_permissions(self, e=None):
        try:
            success = await self.health.request_authorization_async(
                types=[
                    fh.HealthDataTypeAndroid.STEPS,
                    fh.HealthDataTypeAndroid.DISTANCE_DELTA,
                    fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
                ],
                data_access=[
                    fh.DataAccess.READ_WRITE,
                    fh.DataAccess.READ_WRITE,
                    fh.DataAccess.READ_WRITE
                ]
            )
            if success:
                logger.info("Permissions granted!")
                open_snack_bar(self.page, "Permissions granted!", SnackBarType.SUCCESS)
                await self.check_permission()

            else:
                logger.error("Permissions denied.")
                self.debug_icon.add_notify_error(self.page)
                open_snack_bar(self.page, "Permissions denied.", SnackBarType.ERROR)

        except Exception as error:
            logger.error(f"Error requesting permissions.", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page, f"Failed to request permissions: {error}", SnackBarType.ERROR)

        self.page.update()

    async def request_background_read(self, e=None):
        success = await self.health.request_health_data_in_background_authorization_async()

        if success:
            open_snack_bar(
                self.page,
                "Request successfully authorized.",
                SnackBarType.SUCCESS
            )
        else:
            open_snack_bar(self.page, "Background data permission denied.", SnackBarType.ERROR)

    async def insert_health_data(self, e=None):
        try:
            # Inserir registros detalhados associados à sessão
            success = await self.health.write_health_data_async(
                types=fh.HealthDataTypeAndroid.STEPS,
                start_time=self.start_time,
                end_time=self.end_time,
                value=4000.0
            )

            if success:
                await self.health.write_health_data_async(
                    types=fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    value=250.0
                )

                await self.health.write_health_data_async(
                    types=fh.HealthDataTypeAndroid.DISTANCE_DELTA,
                    start_time=self.start_time,
                    end_time=self.end_time,
                    value=3500.0
                )

                logger.info("Exercise session and detailed data entered successfully!")
                open_snack_bar(
                    self.page,
                    "Exercise session and detailed data entered successfully!",
                    SnackBarType.SUCCESS
                )

            else:
                logger.info("Failed to insert health data.")
                open_snack_bar(self.page, "Failed to insert health data.", SnackBarType.INFO)

        except Exception as error:
            logger.error("Error entering exercise session.", exc_info=True)
            self.debug_icon.add_notify_error(self.page)

    async def read_health_data(self, e=None):
        try:
            self.list_view.controls.clear()

            data = await self.health.get_health_data_from_types_async(
                types=[
                    fh.HealthDataTypeAndroid.STEPS,
                    fh.HealthDataTypeAndroid.DISTANCE_DELTA,
                    fh.HealthDataTypeAndroid.TOTAL_CALORIES_BURNED,
                ],
                start_time=self.start_time,
                end_time=self.end_time,
                # recording_method=[fh.RecordingMethod.AUTOMATIC, fh.RecordingMethod.MANUAL]
            )

            await self.extract_data(data)
            self.page.update()

        except Exception as error:
            logger.error(f"Error read_health_data", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page, f"Error read_health_data: {error}", SnackBarType.ERROR)

    async def extract_data(self, data):
        column_ref = ft.Ref[ft.Column]()
        health_data_column_ref = ft.Ref[ft.Column]()

        for health_data in data:
            uuid = health_data.get('uuid')
            start_time_str = health_data.get('dateFrom')
            start_time = datetime.fromisoformat(start_time_str)
            end_time_str = health_data.get('dateTo')
            end_time = datetime.fromisoformat(end_time_str)
            data_type = health_data.get('type')
            value = health_data.get('value')
            numeric_value = value.get('numericValue')
            recording_method = health_data.get('recordingMethod')
            source_name = health_data.get('sourceName')

            self.list_view.controls.append(
                ft.Column(
                    ref=column_ref,
                    controls=[
                        ft.Column(
                            ref=health_data_column_ref,
                            spacing=2,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Text(f'UUID: {uuid}', size=12, selectable=True),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.colors.RED,
                                            on_click=partial(
                                                self.delete_by_uuid,
                                                uuid=uuid,
                                                types=data_type,
                                                column_ref=column_ref,
                                                health_data_column_ref=health_data_column_ref
                                            ),
                                            tooltip="Delete"
                                        )
                                    ]
                                ),
                                ft.Text(f'Start Time: {datetime.strftime(start_time, "%d/%m/%Y | %H:%M:%S")}', size=12,
                                        selectable=True),
                                ft.Text(f'End Time: {datetime.strftime(end_time, "%d/%m/%Y | %H:%M:%S")}', size=12,
                                        selectable=True),
                                ft.Text(f'Type: {data_type}', size=12, selectable=True),
                                ft.Text(f'Value: {numeric_value}', size=12, selectable=True),
                                ft.Text(f'Recording Method: {recording_method}', size=12, selectable=True),
                                ft.Text(f'Source: {source_name}', size=12, selectable=True)
                            ]
                        ),
                    ]
                )
            )

    async def delete_by_uuid(self, e=None, uuid=None, types=None, column_ref=None, health_data_column_ref=None):

        try:
            logger.info(f"health_data_column_ref: {health_data_column_ref}")
            logger.info(f"health_data_column_ref_current: {health_data_column_ref.current}")

            selected_type = (
                    getattr(fh.HealthDataTypeAndroid, types, None)
                    or getattr(fh.HealthDataTypeIOS, types, None)
                    or getattr(fh.HealthWorkoutActivityType, types, None)
            )
            result = await self.health.delete_by_uuid_async(uuid, types=selected_type)

            logger.info(f"Result: {result}")

            if result:
                column_ref.current.controls.remove(health_data_column_ref.current)
                # self.page.update()
                await self.read_health_data()
                open_snack_bar(self.page, "Data deleted successfully!", SnackBarType.SUCCESS)
            else:
                open_snack_bar(self.page, "UUID not found.", SnackBarType.INFO)

        except Exception as error:
            logger.error(f"Error delete_by_uuid", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page, f"Error delete_by_uuid: {error}", SnackBarType.ERROR)

    def handle_date_change(self, e, start_date_field=None, end_date_field=None):
        if start_date_field:
            self.start_time = e.control.value
            start_date_field.value = e.control.value.strftime('%d/%m/%Y')
            start_date_field.update()
            logger.info(f'selected_start_date: {start_date_field.value}')

        if end_date_field:
            self.end_time = e.control.value
            end_date_field.value = e.control.value.strftime('%d/%m/%Y')
            end_date_field.update()
            logger.info(f'selected_end_date: {end_date_field.value}')


    def handle_time_change(self, e, start_time_field=None, end_time_field=None):
        if self.start_time and start_time_field:
            selected_time = e.control.value
            self.start_time = self.start_time.replace(
                hour=selected_time.hour,
                minute=selected_time.minute,
                second=selected_time.second if selected_time.second else 0
            )
            start_time_field.value = selected_time.strftime("%H:%M")
            start_time_field.update()
            logger.info(f'selected_start_time: {selected_time}')

        if self.end_time and end_time_field:
            selected_time = e.control.value
            self.end_time = self.end_time.replace(
                hour=selected_time.hour,
                minute=selected_time.minute,
                second=selected_time.second if selected_time.second else 0
            )
            end_time_field.value = selected_time.strftime("%H:%M")
            end_time_field.update()

            logger.info(f'selected_end_time: {selected_time}')

    def handle_dismissal(self, e):
        self.page.add(ft.Text(f"Dismissed"))

    def handle_error(self, e):
        logger.error(f"handle_error: {e.data}")
        self.debug_icon.add_notify_error(self.page)


class WeightPage(ft.View):
    def __init__(self, page: ft.Page, health: fh.Health):
        super().__init__(route="/record_weight", controls=[])
        self.page = page
        self.health = health
        self.debug_icon = getattr(self.page, 'debug_icon')
        self.health.on_error = self.handle_error
        self.appbar = self.page.appbar
        self.drawer = self.page.drawer
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.has_permissions = False

        self.input_weight = ft.TextField(label="New Record (Kg)", width=250, keyboard_type=ft.KeyboardType.NUMBER,)
        self.history_list = ft.ListView(
            divider_thickness=1,
            expand=True,
            spacing=5,
            padding=10
        )
        self.history_scroll = ft.Container(
            width=self.page.width,
            height=200,
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_300,
            padding=ft.padding.all(10),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.history_list
                ]
            )
        )
        self.average_text = ft.Text()

        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "Request Permissions",
                                on_click=self.request_permissions
                            ),
                        ]
                    ),
                ]
            )
        ]

    def did_mount(self):
        logger.info("did_mount")
        self.page.run_task(self.check_permission)

        async def load_initial_data():
            await asyncio.sleep(0.1)
            if self.has_permissions:
                await self.load_history()
                await self.calculate_average()
                self.page.update()

        self.page.run_task(load_initial_data)

    def will_unmount(self):
        logger.info("will_unmount")

    def build(self):
        logger.info("build")
        return ft.Column(controls=self.controls)

    async def check_permission(self):
        try:
            self.has_permissions = await self.health.has_permissions_async(
                types=[
                    fh.HealthDataTypeAndroid.WEIGHT,
                ],
                data_access=[
                    fh.DataAccess.READ_WRITE
                ]
            )
        except Exception as error:
            logger.error(f"Error checking permissions", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page,f"Error checking permissions: {error}", SnackBarType.ERROR)

        await self.update_controls()

    async def request_permissions(self, e=None):
        try:
            success = await self.health.request_authorization_async(
                types=[
                    fh.HealthDataTypeAndroid.WEIGHT,
                ],
                data_access=[
                    fh.DataAccess.READ_WRITE
                ]
            )
            if success:
                logger.info("Permissions granted!")
                open_snack_bar(self.page, "Permissions granted!", SnackBarType.SUCCESS)
                await self.check_permission()

            else:
                logger.error("Permissions denied.")
                self.debug_icon.add_notify_error(self.page)
                open_snack_bar(self.page, "Permissions denied.", SnackBarType.ERROR)

        except Exception as error:
            logger.error(f"Error requesting permissions.", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            open_snack_bar(self.page, f"Failed to request permissions: {error}", SnackBarType.ERROR)

        self.page.update()

    async def update_controls(self):
        if self.has_permissions:
            self.controls = [
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.input_weight,
                        ft.ElevatedButton("Add", on_click=self.add_weight),
                        ft.Text("Previous Measurements", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        self.history_scroll,
                        ft.Text("Weekly Average", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800),
                        self.average_text,
                    ]
                )
            ]
        else:
            self.controls = [
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.ElevatedButton("Request Permissions", on_click=self.request_permissions),
                            ]
                        ),
                    ]
                )
            ]

        self.page.update()

    async def add_weight(self, e):
        try:
            weight = float(self.input_weight.value.strip())
            now = datetime.now()

            success = await self.health.write_health_data_async(
                types=fh.HealthDataTypeAndroid.WEIGHT,
                start_time=now,
                end_time=now,
                value=weight
            )

            if success:
                self.input_weight.value = None
                await self.load_history()
                await self.calculate_average()
                self.page.update()
            else:
                self.history_list.controls = [ft.Text("Failed to enter the weight.")]
                self.page.update()

        except Exception as error:
            logger.error(f"Error add_weight", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            self.history_list.controls = [ft.Text(f"Error: {error}")]
            self.input_weight.value = None
            self.page.update()

    async def load_history(self):
        try:
            start = datetime.now() - timedelta(days=30)
            end = datetime.now()

            data = await self.health.get_health_data_from_types_async(
                types=[fh.HealthDataTypeAndroid.WEIGHT],
                start_time=start,
                end_time=end
            )

            data.sort(key=lambda d: d.get("dateFrom", ""), reverse=True)

            self.history_list.controls = []

            for d in data:
                weight = d.get("value", {}).get("numericValue", 0)
                timestamp = d.get("dateFrom")

                if weight and timestamp:
                    dt = datetime.fromisoformat(timestamp.split(".")[0])
                    formatted_date = dt.strftime("%d de %B de %Y %H:%M:%S")
                    self.history_list.controls.append(
                        ft.Text(f"{weight:.1f} kilograms {formatted_date}")
                    )

        except Exception as error:
            logger.error(f"Error load_history", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            self.history_list.controls = [ft.Text(f"Error loading history: {error}")]

    async def calculate_average(self):
        try:
            start = datetime.now() - timedelta(days=7)
            end = datetime.now()

            data = await self.health.get_health_data_from_types_async(
                types=[fh.HealthDataTypeAndroid.WEIGHT],
                start_time=start,
                end_time=end
            )

            weights = [
                d.get("value", {}).get("numericValue", 0)
                for d in data if d.get("value", {}).get("numericValue")
            ]
            if weights:
                avg = sum(weights) / len(weights)
                self.average_text.value = f"{avg:.1f} Kg"
            else:
                self.average_text.value = "No recent data"

        except Exception as error:
            logger.error(f"Error calculate_average", exc_info=True)
            self.debug_icon.add_notify_error(self.page)
            self.average_text.value = f"Erro: {error}"

    def handle_error(self, e):
        logger.error(f"handle_error: {e.data}")
        self.debug_icon.add_notify_error(self.page)


def main(page: ft.Page):
    page.title = "Flet Health Example 1"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[ft.Locale("pt", "BR")],
        current_locale=ft.Locale("pt", "BR"),
    )
    debug_icon = DebugNotificationIcon(page, show_console_log)
    setattr(page, "debug_icon", debug_icon)
    health = fh.Health()
    snackbar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=ft.Colors.BLUE_100,
        duration=3000,
    )

    page.overlay.extend([health, snackbar])
    # page.add(health)
    page.update()
    setattr(page, "snackbar", snackbar)

    app_bar = ft.AppBar(
        title=ft.Text(value='Flet Health'),
        bgcolor=ft.Colors.BLUE_700,
        center_title=False,
        color=ft.Colors.WHITE,
        leading=ft.IconButton(
            ft.Icons.MENU,
            on_click=lambda e: open_drawer(e),
        ),
        actions=[
            debug_icon
        ],
        leading_width=50,
    )
    drawer = ft.NavigationDrawer(
        controls=[
            ft.ListView(
                padding=ft.padding.all(10),
                controls=[
                    ft.Container(
                        padding=ft.padding.all(20),
                        content=ft.CircleAvatar(
                            bgcolor=ft.Colors.BLUE_700,
                            radius=30,
                            content=ft.Text("FH", color=ft.Colors.WHITE),
                        ),
                        on_click=lambda e: (page.go("/"), close_drawer(e)),
                    ),
                    ft.Divider(height=10),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.DIRECTIONS_RUN),
                        title=ft.Text("Exercise sessions"),
                        on_click=lambda e: (page.go("/exercise_sessions"), close_drawer(e)),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MONITOR_WEIGHT),
                        title=ft.Text("Record weight"),
                        on_click=lambda e: (page.go("/record_weight"), close_drawer(e)),
                    ),
                    # ft.ListTile(
                    #     leading=ft.Icon(ft.Icons.SETTINGS),
                    #     title=ft.Text("Settings"),
                    #     on_click=lambda e: (page.go("/settings"), close_drawer(e)),
                    # ),
                ],
            )
        ],
        indicator_color=None,
        indicator_shape=ft.StadiumBorder(),
        shadow_color=None,
        elevation=0,
        selected_index=0,
        tile_padding=ft.padding.all(5),
        on_change=lambda e: close_drawer(e)
    )

    page.appbar = app_bar
    page.drawer = drawer

    def open_drawer(e):
        page.drawer.open = True
        page.update()

    def close_drawer(e):
        page.drawer.open = False
        page.update()

    def route_change(route):
        page.views.clear()
        app_bar.title = ft.Text("Flet Health")
        if page.route == "/":
            page.views.append(
                ft.View(
                    appbar=app_bar,
                    drawer=drawer,
                    route="/",
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Column(
                                    expand=True,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text("Welcome to Flet Health!"),
                                        ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                                ft.Text(
                                                    "Health Connect is installed on this device. Use the menu to explore the sample, with each screen demonstrating a different aspect of Health Connect functionality."
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        )
                    ],
                )
            )

        if page.route == "/startup":
            app_bar.title = ft.Text("Flet Health")
            page.views.append(startup_page)

        if page.route == "/exercise_sessions":
            app_bar.title = ft.Text("Exercise Sessions")
            page.views.append(session_page)

        if page.route == "/record_weight":
            app_bar.title = ft.Text("Record Weight")
            page.views.append(weight_page)

        page.update()

    def on_app_lifecycle_change(e: ft.AppLifecycleStateChangeEvent):
        if e.state == ft.AppLifecycleState.RESUME and page.route == "/startup":
            page.run_task(startup_page.check_health_connect)

    startup_page = StartupPage(page, health)
    session_page = SessionsPage(page, health)
    weight_page = WeightPage(page, health)

    page.on_app_lifecycle_state_change = on_app_lifecycle_change

    page.on_route_change = route_change
    page.go("/startup")
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
