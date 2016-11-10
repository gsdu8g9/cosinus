#!/usr/bin/env ruby -wKU

require "vk-ruby"

module Bot

class VkUpdates
    def initialize(vkapi, wait = 25, mode = 0b11101010)
        @vkapi = vkapi
        @updates = []
        @server_values = @vkapi.messages.getLongPollServer
        @server_values["wait"] = wait
        @server_values["mode"] = mode
        @server_values["version"] = 1
    end

    def server_url
        "https://#{@server_values["server"]}?act=a_check&key=#{@server_values["key"]}"\
        "&ts=#{@server_values["ts"]}&wait=#{@server_values["wait"]}"\
        "&version=#{@server_values["version"]}&mode=#{@server_values["mode"]}"
    end

    def _get
        request = Net::HTTP.get URI server_url
        JSON.parse request 
    end

    def _update
        response = _get
        if response.key? "failed"
            case response["failed"]
            when 1
                @server_values["ts"] = response["ts"]
            when 2
                @server_values["key"] = @vkapi.messages.getLongPollServer["key"]
            when 3
                new_values = @vkapi.messages.getLongPollServer
                @server_values["key"] = new_values["key"]
                @server_values["ts"] = new_values["ts"]
            else
                raise ArgumentError
            end
        else
            @server_values["ts"] = response["ts"]
            @updates.push *response["updates"]
        end
    end

    def pop
        while @updates.empty?
            _update
        end
        @updates.shift
    end
end

class VkBot
    attr_accessor :vkapi

    def initialize(config)
        @config = config
        @vkapi = VK::Application.new(access_token: @config["bot"]["token"], version: "5.58")
        @bot_id = @vkapi.users.get[0]['id']
        @chat_queue = VkUpdates.new(@vkapi)
        @chat_plugins = {}

        @config["bot"]['chatplugins'].each do |plugin_name|
            load("chatplugins/#{plugin_name}.rb")
            @chat_plugins[plugin_name] = Object.const_get(plugin_name).const_get("ChatPlugin").new(self)
        end
    end

    def parse_chat
        update = @chat_queue.pop
        @chat_plugins.each do |plugin_name, plugin|
            plugin.call update 
        end
    end
end

end # module Bot
