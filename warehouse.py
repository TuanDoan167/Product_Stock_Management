
LOW_STOCK_LIMIT = 30


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        self.__originalprice = price

    def __str__(self):
        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock.
        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        self.__stock += amount

    def is_stock_empty(self):
        return self.__stock <= 0

    def is_stock_under_limit(self):
        return self.__stock < LOW_STOCK_LIMIT

    def same_category(self, other_product):
        return self.__category == other_product.__category

    def same_price(self, other_product):
        return self.__price == other_product.__price

    def get_category(self):
        return self.__category

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def set_sale(self, category, percent):

        if self.__category != category:
            return False

        else:
            if percent == 0:
                self.__price = self.__originalprice
                return True
            else:
                self.__price = self.__originalprice*(100-percent)/100
                return True


def _read_lines_until(fd, last_line):
    """
    Reads lines from <fd> until the <last_line> is found. Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#' and everything after it on a line).
    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """
    This function reads an input file which must be in the format explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product object as the payload. If an error happens, the return value will be None.
    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:

                lines = _read_lines_until(fd, "BEGIN PRODUCT")

                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")

                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None
                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:

                    keyword, value = line.split(maxsplit=1)  # ValueError possible
                    # print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible
                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.
                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible
                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                if product_code in data:

                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)
                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def main():
    filename = input("Enter database name: ")
    # filename = "products.txt"

    warehouse = read_database(filename)

    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        if "print".startswith(command) and parameters == "":
            for each_product in sorted(warehouse):
                print(warehouse[each_product])

        elif "print".startswith(command) and parameters != "":
            try:
                product_code = int(parameters)
                if product_code not in warehouse:
                    print(f"Error: product \'{parameters}\' can not be printed as it does not exist.")
                else:
                    print(warehouse[product_code])
            except ValueError:
                print(f"Error: product \'{parameters}\' can not be printed as it does not exist.")
                continue

        elif "delete".startswith(command) and parameters != "":
            try:
                product_code = int(parameters)

                if product_code not in warehouse:
                    print(f"Error: product \'{parameters}\' can not be deleted as it does not exist.")

                elif not warehouse[product_code].is_stock_empty():
                    print(f"Error: product \'{product_code}\' can not be deleted as stock remains.")

                else:
                    del warehouse[product_code]

            except ValueError:
                print(f"Error: product \'{parameters}\' can not be deleted as it does not exist.")
                continue

        elif "change".startswith(command) and parameters != "":

            code_amount = parameters.split(" ")
            if len(code_amount) != 2:
                print(f"Error: bad parameters \'{parameters}\' for change command.")
                continue

            try:
                product_code = int(code_amount[0])
            except ValueError:
                print(f"Error: bad parameters \'{parameters}\' for change command.")
                continue

            try:
                amount = int(code_amount[1])
            except ValueError:
                print(f"Error: bad parameters \'{parameters}\' for change command.")
                continue

            if product_code not in warehouse:
                print(f"Error: stock for \'{code_amount[0]}\' can not be changed as it does not exist.")
            else:
                warehouse[product_code].modify_stock_size(amount)

        elif "low".startswith(command) and parameters == "":

            for code in sorted(warehouse):
                if warehouse[code].is_stock_under_limit():
                    print(warehouse[code])

        elif "combine".startswith(command) and parameters != "":
            codes = parameters.split(" ")

            if len(codes) != 2:
                print(f"Error: bad parameters \'{parameters}\' for combine command.")
                continue

            try:
                code1 = int(codes[0])
            except ValueError:
                print(f"Error: bad parameters \'{parameters}\' for combine command.")
                continue

            try:
                code2 = int(codes[1])
            except ValueError:
                print(f"Error: bad parameters \'{parameters}\' for combine command.")
                continue

            if code1 not in warehouse or code2 not in warehouse or code1 == code2:
                print(f"Error: bad parameters \'{parameters}\' for combine command.")
            elif not warehouse[code1].same_category(warehouse[code2]):
                print(f"Error: combining items of different categories \'{warehouse[code1].get_category()}\' and \'{warehouse[code2].get_category()}\'.")
            elif not warehouse[code1].same_price(warehouse[code2]):
                print(f"Error: combining items with different prices {warehouse[code1].get_price()}€ and {warehouse[code2].get_price()}€.")
            else:
                warehouse[code1].modify_stock_size(warehouse[code2].get_stock())
                del warehouse[code2]

        elif "sale".startswith(command) and parameters != "":

            category_percent = parameters.split(" ")
            if len(category_percent) != 2:
                print(f"Error: bad parameters \'{parameters}\' for sale command.")
                continue

            i = 0
            cate = category_percent[0]

            try:
                percent = float(category_percent[1])

            except ValueError:
                print(f"Error: bad parameters \'{parameters}\' for sale command.")
                continue

            for codes in warehouse:
                if warehouse[codes].set_sale(cate, percent):
                    i += 1

            print(f"Sale price set for {i} items.")

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
