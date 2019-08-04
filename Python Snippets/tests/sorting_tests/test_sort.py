import pytest

from sorting import sort

class Test_insert:
    @pytest.mark.parametrize('unsorted,expected', [([3,2,1],[1,2,3])])
    def test_insert_sorts_ascending(self,unsorted,expected):
        sorted = sort.insertion(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Tests_compareto:
    @pytest.mark.parametrize('left,right,expected',[(1,4,True),(9,3,False)])
    def test_compare_defaults_to_ascending(self,left,right,expected):
        assert sort._compareto(left,right,'asc') == expected

    @pytest.mark.parametrize('left,right,expected',[(2,13,True),(34,12,False),(55,55,True)])
    def test_compare_ascending(self,left,right,expected):
        assert sort._compareto(left,right,'asc') == expected

    @pytest.mark.parametrize('left,right,expected',[(0,22,False),(19,-4,True),(22,22,True)])
    def test_compare_descending(self,left,right,expected):
        assert sort._compareto(left,right,'dsc') == expected