class Keyword:
    def __init__(self,value,isNegated) -> None:
        self.value = value
        if isNegated == "true":
            self.isNegated = True
        else:
            self.isNegated = False

    def get_processed_value(self):
        new_keyword = "-" if self.isNegated else ""
        new_keyword += self.value.replace(" ", "")
        return new_keyword