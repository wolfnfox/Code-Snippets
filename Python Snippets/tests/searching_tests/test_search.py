import pytest

from searching import search

class Test_binary:
    @pytest.mark.parametrize('searchlist,item,expected', [([1,3,5,6,7],3,1),([3,4,16,23,40],40,4),([9,10,11,12,13,14],15,-1)])
    def test_binary_finds_unique_element_in_sorted_list(self,searchlist,item,expected):
        i = search.binary(searchlist,item)
        assert i == expected

class Test_linear:
    @pytest.mark.parametrize('searchlist,item,find,expected', [([1,3,5,6,7],3,'first',1),([3,4,16,23,40],40,'first',4),([9,10,11,12,13,14],15,'first',-1)])
    def test_linear_finds_element_in_sorted_list(self,searchlist,item,find,expected):
        i = search.linear(searchlist,item,find)
        assert i == expected