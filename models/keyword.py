class Keyword:
    def __init__(self,value,isNegated) -> None:
        self.value = value
        if isNegated == "true":
            self.isNegated = True
        else:
            self.isNegated = False

    def get_processed_value(self):
        new_keyword = "-" if self.isNegated else ""

        if self.value == "replies":
            new_keyword += "is:reply"
        elif self.value.startswith("from:"):
            new_keyword += self.value.replace(" ", "")
        elif self.value.startswith("#"):
            new_keyword += self.value.replace(" ", "")
        elif self.value.startswith("@"):
            new_keyword += self.value.replace(" ", "")
        else:
            new_keyword += f"'{self.value}'"

        return new_keyword