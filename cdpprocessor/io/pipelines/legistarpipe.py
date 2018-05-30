import requests
from ..checks import *

class LegistarPipe:
    """
    Parameters
    ----------
    city: str
        A Legistar supported city to query against.

    Usage
    ----------
    Contains the default update method for how attributes will be reset to None.
    By setting each attribute in the list of updatable attributes to None,
    the LegistarPipe getattr method will repull the data when requested.

    Contains a self referencing Legistar object get.
    """

    def __init__(self, city):
        """
        Parameters
        ----------
        city: str
            A Legistar supported city to query against.
        """

        self.city = city

        self.updatable = []
        self.update()

    def get_legistar_object(self, query="Bodies"):
        """
        Parameters
        ----------
        self: LegistarPipe
            The LegistarPipe that stores which city to query data for.
        query: str
            Which type of data to query for.
            (Default: "Bodies")

        Output
        ----------
        Returns the json object found from the successful query.
        Unsuccessful queries will raise a ValueError.
        """

        check_city_err = """
    get_legistar_object requires a legistar city name to complete.
    Given: {s_type}
    Please view our documentation for an example.

    Ex: http://webapi.legistar.com/v1/seattle/Bodies
    Would query for a list of bodies against the Seattle Legistar API.
    """

        check_query_err = """
    get_legistar_object requires a query type to complete.
    Given: {s_type}
    Please view our documentation for an example.

    Ex: http://webapi.legistar.com/v1/seattle/Bodies
    Would query for a list of bodies against the Seattle Legistar API.
    """

        check_string(self.city, check_city_err)
        check_string(query, check_query_err)

        url = "http://webapi.legistar.com/v1/{c}/{q}"
        try:
            r = requests.get(url.format(c=city, q=query))

            if r.status_code == 200:
                return r.json()
            else:
                raise ValueError("""
Something went wrong with legistar get.
Status Code: {err}
""".format(err=r.status_code))

        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError("""
Something went wrong with legistar connection.
Could not connect to server.
""")

    def update(self):
        """
        Parameters
        ----------
        self: LegistarPipe
            The LegistarPipe that stores which city to query data for.

        Output
        ----------
        Will set all attributes found in the LegistarPipe's updatable attribute
        list to None as a way to force the next getattr call on an updatable
        attribute to reinitialize the desired attribute.
        """

        for attr in self.updatable:
            setattr(self, attr, None)
