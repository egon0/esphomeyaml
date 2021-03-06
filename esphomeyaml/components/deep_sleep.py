import voluptuous as vol

from esphomeyaml import config_validation as cv, pins
from esphomeyaml.const import CONF_ID, CONF_RUN_CYCLES, CONF_RUN_DURATION, CONF_SLEEP_DURATION, \
    CONF_WAKEUP_PIN
from esphomeyaml.helpers import App, Pvariable, add, exp_gpio_input_pin


def validate_pin_number(value):
    valid_pins = [0, 2, 4, 12, 13, 14, 15, 25, 26, 27, 32, 39]
    if value not in valid_pins:
        raise vol.Invalid(u"Only pins {} support wakeup"
                          u"".format(', '.join(str(x) for x in valid_pins)))
    return value


CONFIG_SCHEMA = vol.Schema({
    cv.GenerateID('deep_sleep'): cv.register_variable_id,
    vol.Optional(CONF_SLEEP_DURATION): cv.positive_time_period,
    vol.Optional(CONF_WAKEUP_PIN): vol.All(cv.only_on_esp32, pins.GPIO_INPUT_PIN_SCHEMA,
                                           pins.schema_validate_number(validate_pin_number)),
    vol.Optional(CONF_RUN_CYCLES): cv.positive_int,
    vol.Optional(CONF_RUN_DURATION): cv.positive_time_period,
})


def to_code(config):
    rhs = App.make_deep_sleep_component()
    deep_sleep = Pvariable('DeepSleepComponent', config[CONF_ID], rhs)
    if CONF_SLEEP_DURATION in config:
        add(deep_sleep.set_sleep_duration(config[CONF_SLEEP_DURATION]))
    if CONF_WAKEUP_PIN in config:
        pin = exp_gpio_input_pin(config[CONF_WAKEUP_PIN])
        add(deep_sleep.set_wakeup_pin(pin))
    if CONF_RUN_CYCLES in config:
        add(deep_sleep.set_run_cycles(config[CONF_RUN_CYCLES]))
    if CONF_RUN_DURATION in config:
        add(deep_sleep.set_run_duration(config[CONF_RUN_DURATION]))


def build_flags(config):
    return '-DUSE_DEEP_SLEEP'
