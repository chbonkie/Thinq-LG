"""------------------for AC"""
import enum
import logging

from typing import Optional

from .device import (
    UNIT_TEMP_CELSIUS,
    UNIT_TEMP_FAHRENHEIT,
    Device,
    DeviceStatus,
)

PROPERTY_TARGET_TEMPERATURE = "target_temperature"
PROPERTY_OPERATION_MODE = "operation_mode"
PROPERTY_FAN_SPEED = "fan_speed"
PROPERTY_VANE_HORIZONTAL = "vane_horizontal"
PROPERTY_VANE_VERTICAL = "vane_vertical"

AC_FLAG_ON = "@ON"
AC_FLAG_OFF = "@OFF"

AC_CTRL_BASIC = ["Control", "basicCtrl"]
AC_CTRL_WIND_DIRECTION = ["Control", "wDirCtrl"]
# AC_CTRL_SETTING = "settingInfo"
# AC_CTRL_WIND_MODE = "wModeCtrl"

SUPPORT_AC_OPERATION_MODE = ["SupportOpMode", "support.airState.opMode"]
SUPPORT_AC_WIND_STRENGTH = ["SupportWindStrength", "support.airState.windStrength"]
AC_STATE_OPERATION = ["Operation", "airState.operation"]
AC_STATE_OPERATION_MODE = ["OpMode", "airState.opMode"]
AC_STATE_CURRENT_TEMP = ["TempCur", "airState.tempState.current"]
AC_STATE_TARGET_TEMP = ["TempCfg", "airState.tempState.target"]
AC_STATE_WIND_STRENGTH = ["WindStrength", "airState.windStrength"]
AC_STATE_WDIR_HSTEP = ["WDirHStep", "airState.wDir.hStep"]
AC_STATE_WDIR_VSTEP = ["WDirVStep", "airState.wDir.vStep"]

CMD_STATE_OPERATION = [AC_CTRL_BASIC, "Set", AC_STATE_OPERATION]
CMD_STATE_OP_MODE = [AC_CTRL_BASIC, "Set", AC_STATE_OPERATION_MODE]
CMD_STATE_TARGET_TEMP = [AC_CTRL_BASIC, "Set", AC_STATE_TARGET_TEMP]
CMD_STATE_WIND_STRENGTH = [AC_CTRL_BASIC, "Set", AC_STATE_WIND_STRENGTH]
CMD_STATE_WDIR_HSTEP = [AC_CTRL_WIND_DIRECTION, "Set", AC_STATE_WDIR_HSTEP]
CMD_STATE_WDIR_VSTEP = [AC_CTRL_WIND_DIRECTION, "Set", AC_STATE_WDIR_VSTEP]

# AC_STATE_WIND_UP_DOWN_V2 = "airState.wDir.upDown"
# AC_STATE_WIND_LEFT_RIGHT_V2 = "airState.wDir.leftRight"

# AC_STATE_CURRENT_HUMIDITY_V2 = "airState.humidity.current"
# AC_STATE_AUTODRY_MODE_V2 = "airState.miscFuncState.autoDry"
# AC_STATE_AIRCLEAN_MODE_V2 = "airState.wMode.airClean"
# AC_STATE_FILTER_MAX_TIME_V2 = "airState.filterMngStates.maxTime"
# AC_STATE_FILTER_REMAIN_TIME_V2 = "airState.filterMngStates.useTime"

DEFAULT_MIN_TEMP = 16
DEFAULT_MAX_TEMP = 30

_LOGGER = logging.getLogger(__name__)


class ACOp(enum.Enum):
    """Whether a device is on or off."""

    OFF = "@AC_MAIN_OPERATION_OFF_W"
    ON = "@AC_MAIN_OPERATION_ON_W"
    RIGHT_ON = "@AC_MAIN_OPERATION_RIGHT_ON_W"  # Right fan only.
    LEFT_ON = "@AC_MAIN_OPERATION_LEFT_ON_W"  # Left fan only.
    ALL_ON = "@AC_MAIN_OPERATION_ALL_ON_W"  # Both fans (or only fan) on.


class ACMode(enum.Enum):
    """The operation mode for an AC/HVAC device."""

    COOL = "@AC_MAIN_OPERATION_MODE_COOL_W"
    DRY = "@AC_MAIN_OPERATION_MODE_DRY_W"
    FAN = "@AC_MAIN_OPERATION_MODE_FAN_W"
    HEAT = "@AC_MAIN_OPERATION_MODE_HEAT_W"
    ACO = "@AC_MAIN_OPERATION_MODE_ACO_W"
    AI = "@AC_MAIN_OPERATION_MODE_AI_W"
    AIRCLEAN = "@AC_MAIN_OPERATION_MODE_AIRCLEAN_W"
    AROMA = "@AC_MAIN_OPERATION_MODE_AROMA_W"
    ENERGY_SAVING = "@AC_MAIN_OPERATION_MODE_ENERGY_SAVING_W"
    ENERGY_SAVER = "@AC_MAIN_OPERATION_MODE_ENERGY_SAVER_W"


class ACFanSpeed(enum.Enum):
    """The fan speed for an AC/HVAC device."""

    SLOW = "@AC_MAIN_WIND_STRENGTH_SLOW_W"
    SLOW_LOW = "@AC_MAIN_WIND_STRENGTH_SLOW_LOW_W"
    LOW = "@AC_MAIN_WIND_STRENGTH_LOW_W"
    LOW_MID = "@AC_MAIN_WIND_STRENGTH_LOW_MID_W"
    MID = "@AC_MAIN_WIND_STRENGTH_MID_W"
    MID_HIGH = "@AC_MAIN_WIND_STRENGTH_MID_HIGH_W"
    HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_W"
    POWER = "@AC_MAIN_WIND_STRENGTH_POWER_W"
    AUTO = "@AC_MAIN_WIND_STRENGTH_AUTO_W"
    NATURE = "@AC_MAIN_WIND_STRENGTH_NATURE_W"
    R_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_RIGHT_W"
    R_MID = "@AC_MAIN_WIND_STRENGTH_MID_RIGHT_W"
    R_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_RIGHT_W"
    L_LOW = "@AC_MAIN_WIND_STRENGTH_LOW_LEFT_W"
    L_MID = "@AC_MAIN_WIND_STRENGTH_MID_LEFT_W"
    L_HIGH = "@AC_MAIN_WIND_STRENGTH_HIGH_LEFT_W"


class ACVSwingMode(enum.Enum):
    """The vertical swing mode for an AC/HVAC device.

    Blades are numbered vertically from 1 (topmost)
    to 6.

    All is 100.
    """

    Off = "@OFF"
    Top = "@1"
    MiddleTop1 = "@2"
    MiddleTop2 = "@3"
    MiddleBottom2 = "@4"
    MiddleBottom1 = "@5"
    Bottom = "@6"
    Swing = "@100"


class ACHSwingMode(enum.Enum):
    """The horizontal swing mode for an AC/HVAC device.
    Blades are numbered horizontally from 1 (leftmost)
    to 5.
    Left half goes from 1-3, and right half goes from
    3-5.
    All is 100.
    """

    Off = "@OFF"
    Left = "@1"
    MiddleLeft = "@2"
    Center = "@3"
    MiddleRight = "@4"
    Right = "@5"
    LeftHalf = "@13"
    RightHalf = "@35"
    Swing = "@100"


class AirConditionerDevice(Device):
    """A higher-level interface for a AC."""

    def __init__(self, client, device, temp_unit=UNIT_TEMP_CELSIUS):
        super().__init__(client, device, AirConditionerStatus(self, None))
        self._temperature_unit = (
            UNIT_TEMP_FAHRENHEIT if temp_unit == UNIT_TEMP_FAHRENHEIT else UNIT_TEMP_CELSIUS
        )
        self._supported_operation = None
        self._supported_op_modes = None
        self._supported_fan_speeds = None
        self._supported_horizontal_swings = None
        self._supported_vertical_swings = None
        self._temperature_range = None

        self._f2c_map = None
        self._c2f_map = None

    def _f2c(self, value):
        """Get a dictionary mapping Fahrenheit to Celsius temperatures for
        this device.

        Unbelievably, SmartThinQ devices have their own lookup tables
        for mapping the two temperature scales. You can get *close* by
        using a real conversion between the two temperature scales, but
        precise control requires using the custom LUT.
        """
        if self._temperature_unit == UNIT_TEMP_CELSIUS:
            return value

        if self._f2c_map is None:
            mapping = self.model_info.value("TempFahToCel").options
            self._f2c_map = {int(f): c for f, c in mapping.items()}
        return self._f2c_map.get(value, value)

    def conv_temp_unit(self, value):
        """Get an inverse mapping from Celsius to Fahrenheit.

        Just as unbelievably, this is not exactly the inverse of the
        `f2c` map. There are a few values in this reverse mapping that
        are not in the other.
        """
        if self._temperature_unit == UNIT_TEMP_CELSIUS:
            return value

        if self._c2f_map is None:
            mapping = self.model_info.value("TempCelToFah").options
            out = {}
            for c, f in mapping.items():
                try:
                    c_num = int(c)
                except ValueError:
                    c_num = float(c)
                out[c_num] = f
            self._c2f_map = out
        return self._c2f_map.get(value, value)

    def _get_supported_operations(self):
        """Get a list of the ACOp Operations the device supports."""

        if not self._supported_operation:
            key = self._get_state_key(AC_STATE_OPERATION)
            mapping = self.model_info.value(key).options
            self._supported_operation = [ACOp(o) for o in mapping.values()]
        return self._supported_operation

    def _supported_on_operation(self):
        """Get the most correct "On" operation the device supports.
        :raises ValueError: If ALL_ON is not supported, but there are
            multiple supported ON operations. If a model raises this,
            its behaviour needs to be determined so this function can
            make a better decision.
        """

        operations = self._get_supported_operations().copy()
        operations.remove(ACOp.OFF)

        # This ON operation appears to be supported in newer AC models
        if ACOp.ALL_ON in operations:
            return ACOp.ALL_ON

        # This ON operation appears to be supported in V2 AC models, to check
        if ACOp.ON in operations:
            return ACOp.ON

        # Older models, or possibly just the LP1419IVSM, do not support ALL_ON,
        # instead advertising only a single operation of RIGHT_ON.
        # Thus, if there's only one ON operation, we use that.
        if len(operations) == 1:
            return operations[0]

        # Hypothetically, the API could return multiple ON operations, neither
        # of which are ALL_ON. This will raise in that case, as we don't know
        # what that model will expect us to do to turn everything on.
        # Or, this code will never actually be reached! We can only hope. :)
        raise ValueError(
            f"could not determine correct 'on' operation:"
            f" too many reported operations: '{str(operations)}'"
        )

    def _get_temperature_range(self):
        if not self._temperature_range:
            key = self._get_state_key(AC_STATE_TARGET_TEMP)
            range_info = self.model_info.value(key)
            if not range_info:
                min_temp = DEFAULT_MIN_TEMP
                max_temp = DEFAULT_MAX_TEMP
            else:
                min_temp = min(range_info.min, DEFAULT_MIN_TEMP)
                max_temp = max(range_info.max, DEFAULT_MAX_TEMP)
            self._temperature_range = [min_temp, max_temp]
        return self._temperature_range

    @property
    def op_modes(self):
        if not self._supported_op_modes:
            key = self._get_state_key(SUPPORT_AC_OPERATION_MODE)
            mapping = self.model_info.value(key).options
            mode_list = [e.value for e in ACMode]
            self._supported_op_modes = [ACMode(o).name for o in mapping.values() if o in mode_list]
        return self._supported_op_modes

    @property
    def fan_speeds(self):
        if self._supported_fan_speeds is None:
            key = self._get_state_key(SUPPORT_AC_WIND_STRENGTH)
            mapping = self.model_info.value(key).options
            mode_list = [e.value for e in ACFanSpeed]
            self._supported_fan_speeds = [ACFanSpeed(o).name for o in mapping.values() if o in mode_list]
        return self._supported_fan_speeds

    @property
    def horizontal_swing_modes(self):
        if self._supported_horizontal_swings is None:
            key = self._get_state_key(AC_STATE_WDIR_HSTEP)
            values = self.model_info.value(key)
            if not hasattr(values, "options"):
                self._supported_horizontal_swings = []
                return self._supported_horizontal_swings

            mapping = values.options
            mode_list = [e.value for e in ACHSwingMode]
            self._supported_horizontal_swings = [
                ACHSwingMode(o).name for o in mapping.values() if o in mode_list
            ]
        return self._supported_horizontal_swings

    @property
    def vertical_swing_modes(self):
        if self._supported_vertical_swings is None:
            key = self._get_state_key(AC_STATE_WDIR_VSTEP)
            values = self.model_info.value(key)
            if not hasattr(values, "options"):
                self._supported_vertical_swings = []
                return self._supported_vertical_swings

            mapping = values.options
            mode_list = [e.value for e in ACVSwingMode]
            self._supported_vertical_swings = [
                ACVSwingMode(o).name for o in mapping.values() if o in mode_list
            ]
        return self._supported_vertical_swings

    @property
    def temperature_unit(self):
        return self._temperature_unit

    @property
    def target_temperature_step(self):
        return 1

    @property
    def target_temperature_min(self):
        temp_range = self._get_temperature_range()
        if not temp_range:
            return None
        return self.conv_temp_unit(temp_range[0])

    @property
    def target_temperature_max(self):
        temp_range = self._get_temperature_range()
        if not temp_range:
            return None
        return self.conv_temp_unit(temp_range[1])

    def power(self, turn_on):
        """Turn on or off the device (according to a boolean)."""

        op = self._supported_on_operation() if turn_on else ACOp.OFF
        keys = self._get_cmd_keys(CMD_STATE_OPERATION)
        op_value = self.model_info.enum_value(keys[2], op.value)
        self.set(keys[0], keys[1], key=keys[2], value=op_value)

    def set_op_mode(self, mode):
        """Set the device's operating mode to an `OpMode` value."""

        if mode not in self.op_modes:
            raise ValueError(f"Invalid operating mode: {mode}")
        keys = self._get_cmd_keys(CMD_STATE_OP_MODE)
        mode_value = self.model_info.enum_value(keys[2], ACMode[mode].value)
        self.set(keys[0], keys[1], key=keys[2], value=mode_value)

    def set_fan_speed(self, speed):
        """Set the fan speed to a value from the `ACFanSpeed` enum."""

        if speed not in self.fan_speeds:
            raise ValueError(f"Invalid fan speed: {speed}")
        keys = self._get_cmd_keys(CMD_STATE_WIND_STRENGTH)
        speed_value = self.model_info.enum_value(keys[2], ACFanSpeed[speed].value)
        self.set(keys[0], keys[1], key=keys[2], value=speed_value)

    def set_horizontal_swing_mode(self, mode):
        """Set the hor swing to a value from the `ACHSwingMode` enum."""

        if mode not in self.horizontal_swing_modes:
            raise ValueError(f"Invalid horizontal swing mode: {mode}")
        keys = self._get_cmd_keys(CMD_STATE_WDIR_HSTEP)
        swing_mode = self.model_info.enum_value(keys[2], ACHSwingMode[mode].value)
        self.set(keys[0], keys[1], key=keys[2], value=swing_mode)

    def set_vertical_swing_mode(self, mode):
        """Set the vertical swing to a value from the `ACVSwingMode` enum."""

        if mode not in self.vertical_swing_modes:
            raise ValueError(f"Invalid vertical swing mode: {mode}")
        keys = self._get_cmd_keys(CMD_STATE_WDIR_VSTEP)
        swing_mode = self.model_info.enum_value(keys[2], ACVSwingMode[mode].value)
        self.set(keys[0], keys[1], key=keys[2], value=swing_mode)

    def set_target_temp(self, temp):
        """Set the device's target temperature in Celsius degrees."""

        range_info = self._get_temperature_range()
        conv_temp = self._f2c(temp)
        if range_info and not (range_info[0] <= conv_temp <= range_info[1]):
            raise ValueError(f"Target temperature out of range: {temp}")
        keys = self._get_cmd_keys(CMD_STATE_TARGET_TEMP)
        self.set(keys[0], keys[1], key=keys[2], value=conv_temp)

    def set(self, ctrl_key, command, *, key=None, value=None, data=None):
        """Set a device's control for `key` to `value`."""
        super().set(ctrl_key, command, key=key, value=value, data=data)
        if self._status:
            self._status.update_status(key, value)

    def reset_status(self):
        self._status = AirConditionerStatus(self, None)
        return self._status

    def poll(self) -> Optional["AirConditionerStatus"]:
        """Poll the device's current state."""

        res = self.device_poll()
        if not res:
            return None

        self._status = AirConditionerStatus(self, res)
        return self._status


class AirConditionerStatus(DeviceStatus):
    """Higher-level information about a AC's current status."""

    @staticmethod
    def _str_to_num(s):
        """Convert a string to either an `int` or a `float`.

        Troublingly, the API likes values like "18", without a trailing
        ".0", for whole numbers. So we use `int`s for integers and
        `float`s for non-whole numbers.
        """
        if not s:
            return None

        f = float(s)
        if f == int(f):
            return int(f)
        else:
            return f

    def _str_to_temp(self, s):
        """Convert a string to either an `int` or a `float` temperature."""
        temp = self._str_to_num(s)
        return self._device.conv_temp_unit(temp)

    def _get_state_key(self, key_name):
        if isinstance(key_name, list):
            return key_name[1 if self.is_info_v2 else 0]
        return key_name

    def _get_operation(self):
        key = self._get_state_key(AC_STATE_OPERATION)
        try:
            return ACOp(self.lookup_enum(key, True))
        except ValueError:
            return None

    @property
    def is_on(self):
        op = self._get_operation()
        if not op:
            return False
        return op != ACOp.OFF

    @property
    def operation(self):
        op = self._get_operation()
        if not op:
            return None
        return op.name

    @property
    def operation_mode(self):
        key = self._get_state_key(AC_STATE_OPERATION_MODE)
        try:
            return ACMode(self.lookup_enum(key, True)).name
        except ValueError:
            return None

    @property
    def fan_speed(self):
        key = self._get_state_key(AC_STATE_WIND_STRENGTH)
        try:
            return ACFanSpeed(self.lookup_enum(key, True)).name
        except ValueError:
            return None

    @property
    def horizontal_swing_mode(self):
        key = self._get_state_key(AC_STATE_WDIR_HSTEP)
        try:
            return ACHSwingMode(self.lookup_enum(key, True)).name
        except ValueError:
            return None

    @property
    def vertical_swing_mode(self):
        key = self._get_state_key(AC_STATE_WDIR_VSTEP)
        try:
            return ACVSwingMode(self.lookup_enum(key, True)).name
        except ValueError:
            return None

    @property
    def current_temp(self):
        key = self._get_state_key(AC_STATE_CURRENT_TEMP)
        return self._str_to_temp(self._data.get(key))

    @property
    def target_temp(self):
        key = self._get_state_key(AC_STATE_TARGET_TEMP)
        return self._str_to_temp(self._data.get(key))

    def _update_features(self):
        return
