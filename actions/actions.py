from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
import requests
import json
from datetime import datetime

class ActionControlDevice(Action):
    """控制智能设备的Action"""

    def name(self) -> Text:
        return "action_control_device"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        device_type = tracker.get_slot("device_type")
        location = tracker.get_slot("location")
        action = tracker.get_slot("action")
        value = tracker.get_slot("value")
        color = tracker.get_slot("color")
        temperature = tracker.get_slot("temperature")
        brightness = tracker.get_slot("brightness")

        # 构建设备控制请求
        device_control_data = {
            "device_type": device_type,
            "location": location,
            "action": action,
            "value": value,
            "color": color,
            "temperature": temperature,
            "brightness": brightness
        }

        try:
            # 调用后端API控制设备
            response = requests.post(
                "http://localhost:5000/api/devices/control",
                json=device_control_data,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    dispatcher.utter_message(
                        text=f"好的，已经为你{action}{location}的{device_type}。"
                    )
                else:
                    dispatcher.utter_message(
                        text=f"抱歉，控制{location}的{device_type}失败：{result.get('message', '未知错误')}"
                    )
            else:
                dispatcher.utter_message(
                    text=f"抱歉，设备控制服务暂时不可用。"
                )
                
        except requests.exceptions.RequestException:
            # 如果后端服务不可用，返回模拟响应
            dispatcher.utter_message(
                text=f"好的，已经为你{action}{location}的{device_type}。（模拟模式）"
            )

        return []


class ActionGetWeather(Action):
    """获取天气信息的Action"""

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            # 调用天气API（这里使用模拟数据）
            weather_info = {
                "temperature": "25°C",
                "condition": "晴天",
                "humidity": "60%",
                "wind": "微风"
            }
            
            dispatcher.utter_message(
                text=f"今天天气{weather_info['condition']}，温度{weather_info['temperature']}，湿度{weather_info['humidity']}，{weather_info['wind']}。"
            )
            
        except Exception as e:
            dispatcher.utter_message(
                text="抱歉，暂时无法获取天气信息。"
            )

        return []


class ActionGetTime(Action):
    """获取当前时间的Action"""

    def name(self) -> Text:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        dispatcher.utter_message(text=f"现在是{current_time}。")

        return []


class ActionGetDeviceStatus(Action):
    """获取设备状态的Action"""

    def name(self) -> Text:
        return "action_get_device_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        device_type = tracker.get_slot("device_type")
        location = tracker.get_slot("location")

        try:
            # 调用后端API获取设备状态
            response = requests.get(
                f"http://localhost:5000/api/devices/status",
                params={"device_type": device_type, "location": location},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get("status", "未知")
                dispatcher.utter_message(
                    text=f"{location}的{device_type}当前状态是：{status}。"
                )
            else:
                dispatcher.utter_message(
                    text="抱歉，无法获取设备状态。"
                )
                
        except requests.exceptions.RequestException:
            # 模拟响应
            dispatcher.utter_message(
                text=f"{location}的{device_type}当前状态是：开启。（模拟模式）"
            )

        return []


class ValidateDeviceControlForm(FormValidationAction):
    """验证设备控制表单的Action"""

    def name(self) -> Text:
        return "validate_device_control_form"

    def validate_device_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """验证设备类型"""
        
        valid_devices = ["灯", "灯光", "台灯", "吊灯", "空调", "窗帘", "电视", "音响"]
        
        if slot_value and slot_value.lower() in [d.lower() for d in valid_devices]:
            return {"device_type": slot_value}
        else:
            dispatcher.utter_message(text="抱歉，我不支持控制这种设备。支持的设备有：灯、空调、窗帘、电视等。")
            return {"device_type": None}

    def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """验证位置"""
        
        valid_locations = ["客厅", "卧室", "厨房", "书房", "餐厅", "阳台", "卫生间"]
        
        if slot_value and slot_value in valid_locations:
            return {"location": slot_value}
        else:
            dispatcher.utter_message(text="请指定一个有效的房间位置，如：客厅、卧室、厨房等。")
            return {"location": None}

    def validate_action(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """验证操作动作"""
        
        valid_actions = ["打开", "关闭", "开", "关", "调亮", "调暗", "调高", "调低", "拉开", "拉上"]
        
        if slot_value and slot_value in valid_actions:
            return {"action": slot_value}
        else:
            dispatcher.utter_message(text="请指定一个有效的操作，如：打开、关闭、调亮、调暗等。")
            return {"action": None}

