from aiogram.utils.callback_data import CallbackData

group_callback = CallbackData("group", "group_id", "role")
show_callback = CallbackData("show", "data_type", "user_role")
add_lab_callback = CallbackData("add_lab", "group_id", "user_role")
check_lab_callback = CallbackData("check_lab", "lab_id", "status")
stats_callback = CallbackData("stats", "group_id", "user_role")
