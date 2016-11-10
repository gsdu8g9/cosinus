module HelloWorld
    class ChatPlugin
        def initialize(botref)
            @bot = botref
        end

        def call(event)
            puts "Call 1"
            if event[0] == 4 and event[6] == "/rubyping"
                puts "Call 2"
                # @bot.vkapi.messages.send message: "Pong!", peer_id: event[3]
                @bot.vkapi.vk_call "messages.send", message: "RubyPong!", peer_id: event[3]
            end
        end
    end
end
