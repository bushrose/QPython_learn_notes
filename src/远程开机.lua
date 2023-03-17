import "java.net.InetAddress"
import "java.net.DatagramPacket"
import "java.net.DatagramSocket"
import "java.lang.Integer"
import "java.lang.System"


domainName = "123.145.8.199"
-- mac地址是冒号为分隔符的格式,不要用其他格式
macAddress = "04:7C:16:01:21:85"












-- 定义元类
WakeUpOnline={}

-- 定义new方法
function WakeUpOnline:new(o)
    o = o or {}
    setmetatable(o, self)
    self.__index = self
    return o
end




-- 定义远程唤醒方法
function WakeUpOnline:wakeUp(host, mac, port)
    --[[
     在外网远程打开局域网内的电脑 本方法仅用于外网. 不适用于无线网卡
     {string} host     路由器的wan口iP或者域名
     {string} mac      被远程开机电脑的网卡mac地址
     {int} port        开机端口号, 内网为9号端口. 这里填你映射出去的端口号   
    --]]
    local macBytes = WakeUpOnline:getMacBytes(mac);
    print(macBytes)
    local bytes = util.java.array('byte', 6 + 16 * macBytes.length)
    for i = 1, 6, 1 do
        bytes[i] = 0xff - 256;
    end

    for i = 6, bytes.length-1, macBytes.length do
        System.arraycopy(macBytes, 0, bytes, i, macBytes.length)
    end

    local address = InetAddress.getByName(host);
    local packet = DatagramPacket(bytes, bytes.length, address, port)
    local socket = DatagramSocket()
    socket.send(packet);
    socket.close();
    return "wol_package_sent_success";
end



function WakeUpOnline:getMacBytes(mac)
    local bytes = util.java.array('byte', 6);;
    local hex = mac.split(":");
    if hex.length ~= 6 then
        error("Invalid MAC address.")
    end
    for i = 1, 6, 1 do
        local int = Integer.parseInt(hex[i], 16);
        if int > 127 then
            int = int - 256
        end
        bytes[i] = int
    end
    return bytes
end



function errorHandler(err)
    print( "ERROR:", err )
end


status=xpcall(WakeUpOnline:wakeUp,errorHandler)
print(status)
status=xpcall(WakeUpOnline:getMacBytes,errorHandler)
print(status)



wol = WakeUpOnline:new(nil)
res = wol.wakeUp(domainName, macAddress,9)
print(res);









