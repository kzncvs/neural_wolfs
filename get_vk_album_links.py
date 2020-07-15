import vk_api
import config

vk_session = vk_api.VkApi(config.vk_phone_number, config.vk_password)
vk_session.auth()

vk = vk_session.get_api()
