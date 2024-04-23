from .models import CalendaData
from .calculator import find_ten_god, find_stem_branch_ten_god,descending_tens,to_hanja

class Msr_Calculator():

    def __init__(self):
        pass

    def getAll(self, year, month, day, time, sl, gen):
        if sl == "양력":
            birthdata = CalendaData.objects.using('manseryuk').filter(
                cd_sy=year, cd_sm=month, cd_sd=day
            )
        else:
            birthdata = CalendaData.objects.using('manseryuk').filter(
                cd_ly=year, cd_lm=month, cd_ld=day
            )

        if sl == "음력윤달":
            data = birthdata[1]
        else:
            data = birthdata[0]

        outdata = {
            "s_year": data.cd_sy,
            "s_month": data.cd_sm,
            "s_day": data.cd_sd,
            "l_year": data.cd_ly,
            "l_month": data.cd_lm,
            "l_day": data.cd_ld,
            "year_gan_ch": data.cd_hyganjee[0],
            "year_ji_ch": data.cd_hyganjee[1],
            "year_gan_kr": data.cd_kyganjee[0],
            "year_ji_kr": data.cd_kyganjee[1],
            "month_gan_ch": data.cd_hmganjee[0],
            "month_ji_ch": data.cd_hmganjee[1],
            "month_gan_kr": data.cd_kmganjee[0],
            "month_ji_kr": data.cd_kmganjee[1],
            "day_gan_ch": data.cd_hdganjee[0],
            "day_ji_ch": data.cd_hdganjee[1],
            "day_gan_kr": data.cd_kdganjee[0],
            "day_ji_kr": data.cd_kdganjee[1],
            "ddi_kor": data.cd_ddi,
            "sol_plan": data.cd_sol_plan,
            "lunar_plan": data.cd_lun_plan,
        }
        outdata["time_ji_kr"] = time
        outdata["time_gan_kr"] = self.get_time_gan(
            outdata["day_gan_kr"], outdata["time_ji_kr"]
        )
        outdata["time_gan_ch"] = self.gankr_to_ch(outdata["time_gan_kr"])
        outdata["time_ji_ch"] = self.jikr_to_ch(outdata["time_ji_kr"])
        outdata["gender"] = gen
        outdata["daewoon"] = self.getDaewoon(
            outdata["gender"], outdata["year_gan_kr"],
            outdata["month_gan_kr"], outdata["month_ji_kr"]
        )
        outdata["daewoon_num"] = self.daewoonNum(
            year, month, day, sl, outdata["daewoon"][0]
        )
        outdata["daewoon_num_list"] = descending_tens(outdata["daewoon_num"])
        outdata["time_gan10"] = find_ten_god(outdata["day_gan_kr"],outdata["time_gan_kr"])
        outdata["month_gan10"] = find_ten_god(outdata["day_gan_kr"],outdata["month_gan_kr"])
        outdata["year_gan10"] = find_ten_god(outdata["day_gan_kr"],outdata["year_gan_kr"])
        outdata["time_ji10"] = find_stem_branch_ten_god(outdata["day_gan_kr"],outdata["time_ji_kr"])
        outdata["day_ji10"] = find_stem_branch_ten_god(outdata["day_gan_kr"],outdata["day_ji_kr"])
        outdata["month_ji10"] = find_stem_branch_ten_god(outdata["day_gan_kr"],outdata["month_ji_kr"])
        outdata["year_ji10"] = find_stem_branch_ten_god(outdata["day_gan_kr"],outdata["year_ji_kr"])
        return outdata

    def getDaewoon(self, gen, ygan, mgan, mji):
        YANGGAN = ["갑", "병", "무", "경", "임"]
        EUMGAN = ["을", "정", "기", "신", "계"]
        CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

        if (gen == "남" and ygan in YANGGAN) or (gen == "여" and ygan in EUMGAN):
            data = ["순행"]
            data_gan = []
            data_ji = []
            for i in range(len(CHEONGAN)):
                if CHEONGAN[i] == mgan:
                    start = i + 1
            for i in range(10):
                data_gan.append(CHEONGAN[start % 10])
                start += 1

            for i in range(len(JIJI)):
                if JIJI[i] == mji:
                    start = i + 1

            for i in range(10):
                data_ji.append(JIJI[start % 12])
                start += 1

            data_gan = to_hanja(data_gan)
            data_ji = to_hanja(data_ji)
            data.append(list(reversed(data_gan)))
            data.append(list(reversed(data_ji)))

            return data

        elif (gen == "남" and ygan in EUMGAN) or (gen == "여" and ygan in YANGGAN):
            data = ["역행"]
            data_gan = []
            data_ji = []
            for i in range(len(CHEONGAN)):
                if CHEONGAN[i] == mgan:
                    start = i - 1

            for i in range(10):
                data_gan.append(CHEONGAN[start % 10])
                start -= 1

            for i in range(len(JIJI)):
                if JIJI[i] == mji:
                    start = i - 1

            for i in range(10):
                data_ji.append(JIJI[start % 12])
                start -= 1
            data_gan = to_hanja(data_gan)
            data_ji = to_hanja(data_ji)
            data.append(list(reversed(data_gan)))
            data.append(list(reversed(data_ji)))

            return data
        
    
    # def getDaewoon(self, gender, yearGan, monthGan, dayJi):
    #     YANG_GAN = ["갑", "병", "무", "경", "임"]
    #     EUM_GAN = ["을", "정", "기", "신", "계"]
    #     ALL_GAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    #     ALL_JI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

    #     direction = None
    #     if (gender == "남" and yearGan in YANG_GAN) or (gender == "여" and yearGan in EUM_GAN):
    #         direction = "순행"
    #     elif (gender == "남" and yearGan in EUM_GAN) or (gender == "여" and yearGan in YANG_GAN):
    #         direction = "역행"

    #     if not direction:
    #         raise ValueError("Invalid gender or year Gan")

    #     data = [direction]

    #     def rotate_elements(elements, start_index, reverse=False):
    #         length = len(elements)
    #         rotated = []
    #         step = -1 if reverse else 1
    #         index = start_index
    #         for _ in range(length):
    #             rotated.append(elements[index % length])
    #             index += step
    #         return rotated

    #     start_gan = ALL_GAN.index(monthGan)
    #     start_ji = ALL_JI.index(dayJi)

    #     if direction == "순행":
    #         rotated_gan = rotate_elements(ALL_GAN, start_gan + 1)
    #         rotated_ji = rotate_elements(ALL_JI, start_ji + 1)
    #     else:
    #         rotated_gan = rotate_elements(ALL_GAN, start_gan - 1, reverse=True)
    #         rotated_ji = rotate_elements(ALL_JI, start_ji - 1, reverse=True)

    #     data.append(self.to_hanja(rotated_gan))
    #     data.append(self.to_hanja(rotated_ji))

    #     return data



    def daewoonNum(self, year, month, day, sl, way):
        JEOLGI = ["입춘", "경칩", "청명", "입하", "망종", "소서",
                  "입추", "백로", "한로", "입동", "대설", "소한"]
        if sl == "양력":
            birthdata = CalendaData.objects.using('manseryuk').filter(
                cd_sy=year, cd_sm=month, cd_sd=day
            )
        else:
            birthdata = CalendaData.objects.using('manseryuk').filter(
                cd_ly=year, cd_lm=month, cd_ld=day
            )
        start_spot = birthdata[0].cd_no - 35
        temp_data_list = CalendaData.objects.using('manseryuk').filter(
            cd_no__gt=start_spot, cd_no__lt=start_spot+70
        )
        temp_data = []
        for i in range(len(temp_data_list)):
            if temp_data_list[i].cd_kterms in JEOLGI:
                temp_data.append(temp_data_list[i])
        if way == "순행":
            for i in range(len(temp_data)):
                if birthdata[0].cd_no < temp_data[i].cd_no:
                    daewoon_num = round(
                        (temp_data[i].cd_no - birthdata[0].cd_no) / 3, 1)
                    return daewoon_num
        else:
            for i in range(len(temp_data)):
                if birthdata[0].cd_no > temp_data[len(temp_data)-1-i].cd_no:
                    daewoon_num = round(
                        (birthdata[0].cd_no -
                         temp_data[len(temp_data)-1-i].cd_no) / 3, 1)
                    return daewoon_num

    def get_time_gan(self, day_gan_kr, time_ji):
        CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
        for i in range(len(JIJI)):
            if JIJI[i] == time_ji:
                time_ji_num = i

        if day_gan_kr == "갑" or day_gan_kr == "기":
            return CHEONGAN[time_ji_num % 10]
        if day_gan_kr == "을" or day_gan_kr == "경":
            return CHEONGAN[(time_ji_num + 2) % 10]
        if day_gan_kr == "병" or day_gan_kr == "신":
            return CHEONGAN[(time_ji_num + 4) % 10]
        if day_gan_kr == "정" or day_gan_kr == "임":
            return CHEONGAN[(time_ji_num + 6) % 10]
        if day_gan_kr == "무" or day_gan_kr == "계":
            return CHEONGAN[(time_ji_num + 8) % 10]

    def gankr_to_ch(self, gankr):
        CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        CHEONGAN_CH = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        for i in range(len(CHEONGAN)):
            if CHEONGAN[i] == gankr:
                return CHEONGAN_CH[i]

    def jikr_to_ch(self, jikr):
        JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
        JIJI_CH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        for i in range(len(JIJI)):
            if JIJI[i] == jikr:
                return JIJI_CH[i]
            
            

