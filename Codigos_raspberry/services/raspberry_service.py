class RaspberryService:

    @staticmethod
    def obtener_id():

        with open("/proc/cpuinfo", "r") as f:

            for line in f:

                if line.startswith("Serial"):

                    return line.split(":")[1].strip()

        return None