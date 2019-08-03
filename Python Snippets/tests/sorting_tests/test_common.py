import pytest

from sorting import common

class Tests_compare:
    @pytest.mark.parametrize('left,right,expected',[(1,4,True),(9,3,False)])
    def test_compare_defaults_to_ascending(self,left,right,expected):
        assert common._compareto(left,right,'asc') == expected

    @pytest.mark.parametrize('left,right,expected',[(2,13,True),(34,12,False),(55,55,True)])
    def test_compare_ascending(self,left,right,expected):
        assert common._compareto(left,right,'asc') == expected

    @pytest.mark.parametrize('left,right,expected',[(0,22,False),(19,-4,True),(22,22,True)])
    def test_compare_descending(self,left,right,expected):
        assert common._compareto(left,right,'dsc') == expected