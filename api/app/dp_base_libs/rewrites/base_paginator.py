from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger, EmptyPage


class DPBasePaginator(Paginator):
    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.num_pages:
            if number == 1 and self.allow_empty_first_page:
                pass
            elif number > self.num_pages:
                number = self.num_pages
            else:
                raise EmptyPage('That page contains no results')
        return number