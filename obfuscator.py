import random
import string
import base64
import time

class SttarObfuscator:
    def __init__(self):
        self.intensity = "Extreme"

    def generate_random_var(self, length=16):
        first = random.choice(string.ascii_letters + "_")
        rest = ''.join(random.choices(string.ascii_letters + string.digits + "_", k=length-1))
        return first + rest

    def generate_key(self, length=48):
        return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+", k=length))

    def xor_bytes(self, data: bytes, key: str) -> bytes:
        key_bytes = (key * (len(data) // len(key) + 1)).encode('utf-8')[:len(data)]
        return bytes(a ^ b for a, b in zip(data, key_bytes))

    def multi_xor_encrypt(self, data: str) -> tuple:
        key1 = self.generate_key(40)
        key2 = self.generate_key(40)
        key3 = self.generate_key(32)

        data_bytes = data.encode('utf-8')
        step1 = self.xor_bytes(data_bytes, key1)
        step2 = self.xor_bytes(step1, key2)
        step3 = self.xor_bytes(step2, key3)
        
        encrypted_b64 = base64.b64encode(step3).decode('ascii')
        return encrypted_b64, key1, key2, key3

    def create_ultra_vm(self, encrypted_b64: str, key1: str, key2: str, key3: str) -> str:
        vm_name = self.generate_random_var(12)
        junk_vars = [self.generate_random_var() for _ in range(28)]

        junk_layer = ""
        for v in junk_vars:
            mult = random.randint(2, 9)
            junk_layer += f'local {v} = {{}}; for i=1,math.random(8,40) do {v}[i] = function(x) return x * {mult} end end\n'

        # Clean Lua code with proper escaping
        vm = f'''-- Sttar Obfuscator Ultra VM | Build {int(time.time())}
local {vm_name} = {{}}
local function h(x) return string.char(x) end

-- HEAVY JUNK LAYER
{junk_layer}

local function b64_decode(input)
    local b64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    local t = {{}}
    for i = 1, #b64chars do
        t[string.sub(b64chars, i, i)] = i - 1
    end
    local out = {{}}
    local p = 0
    local n = 0
    for i = 1, #input do
        local c = string.sub(input, i, i)
        if c == "=" then break end
        local val = t[c]
        if val then
            p = p * 64 + val
            n = n + 1
            if n == 4 then
                out[#out+1] = h(p // 65536)
                out[#out+1] = h((p // 256) % 256)
                out[#out+1] = h(p % 256)
                p = 0
                n = 0
            end
        end
    end
    return table.concat(out)
end

local function decrypt(data_b64, k1, k2, k3)
    local data = b64_decode(data_b64)
    local result = {{}}
    for i = 1, #data do
        local byte = string.byte(data, i)
        local k = string.byte(k1, ((i-1) % #k1) + 1)
        result[i] = h(byte \~ k)
    end
    local s1 = table.concat(result)

    local result2 = {{}}
    for i = 1, #s1 do
        local byte = string.byte(s1, i)
        local k = string.byte(k2, ((i-1) % #k2) + 1)
        result2[i] = h(byte \~ k)
    end
    local s2 = table.concat(result2)

    local result3 = {{}}
    for i = 1, #s2 do
        local byte = string.byte(s2, i)
        local k = string.byte(k3, ((i-1) % #k3) + 1)
        result3[i] = h(byte \~ k)
    end
    return table.concat(result3)
end

if getgenv then getgenv().SttarProtected = true end

local payload = "{encrypted_b64}"
local k1 = "{key1}"
local k2 = "{key2}"
local k3 = "{key3}"

local success, raw_code = pcall(decrypt, payload, k1, k2, k3)
if not success or not raw_code then
    error("Sttar VM: Decryption Failed")
end

local func, err = load(raw_code) or loadstring(raw_code)
if not func then
    error("Sttar VM: Load Failed - " .. (err or "Unknown"))
end

return func()
'''
        return vm

    def obfuscate(self, code: str, intensity: str = "Extreme") -> tuple:
        original_size = len(code)
        if len(code) > 120000:
            raise ValueError("Script too large (max \~120k chars)")

        junk_prefix = "\n".join([f"local {self.generate_random_var()} = function() end" for _ in range(18)])
        protected_code = junk_prefix + "\n\n" + code

        encrypted_b64, k1, k2, k3 = self.multi_xor_encrypt(protected_code)
        final_code = self.create_ultra_vm(encrypted_b64, k1, k2, k3)

        obfuscated_size = len(final_code)
        compression = round((1 - obfuscated_size / max(original_size, 1)) * 100, 1)

        return final_code, {
            "original": original_size,
            "obfuscated": obfuscated_size,
            "compression": compression,
    }
