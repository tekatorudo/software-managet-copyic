class GetData:
    @staticmethod
    def set_model(lst :list[list[str]]):
        result_list = []
        print(lst)
        # Lặp qua từng danh sách con trong danh sách chuỗi ban đầu
        global bin
        for string_item in lst:
            # Tạo một từ điển chứa thông tin từ danh sách chuỗi
            item_dict = {}
            # print("string_item[3:]",string_item[3:])
            print("string_item[:3]",string_item[5][-3:])
            if 'BIN_FILE' in string_item:
                bin = string_item[5]
            elif 'CHECKSUM&PROJECT' in string_item:
                item_dict = {
                    "model": string_item[0],
                    "PN": string_item[1],
                    "MPN": string_item[2],
                    "LocationPCB": string_item[3],
                    "Binfile":bin,
                    "Machine": string_item[5],
                    "checksum": "chek" if len(string_item) > 6 else None,
                    "project": string_item[6] if len(string_item) > 6 and string_item[6][-3:] =='txt' else None
                }

            # Thêm từ điển vào danh sách kết quả
            result_list.append(item_dict)

        # In danh sách kết quả
        for item in result_list:
            print(item)

