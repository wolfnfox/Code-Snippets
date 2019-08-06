import pytest

from sorting import sort

class Test_bubble:
    @pytest.mark.parametrize('unsorted,expected', [([2,3,3,2,4,5,1],[1,2,2,3,3,4,5])])
    def test_bubble_sorts_ascending(self,unsorted,expected):
        sorted = sort.bubble(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Test_insertion:
    @pytest.mark.parametrize('unsorted,expected', [([2,3,3,2,4,5,1],[1,2,2,3,3,4,5])])
    def test_insertion_sorts_ascending(self,unsorted,expected):
        sorted = sort.insertion(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Test_merge:
    @pytest.mark.parametrize('unsorted,expected', [([2,3,3,2,4,5,1],[1,2,2,3,3,4,5])])
    def test_merge_sorts_ascending(self,unsorted,expected):
        sorted = sort.merge(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Test_quick:
    @pytest.mark.parametrize('unsorted,expected', [([2,3,3,2,4,5,1],[1,2,2,3,3,4,5])])
    def test_quick_sorts_ascending(self,unsorted,expected):
        sorted = sort.quick(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Test_selection:
    @pytest.mark.parametrize('unsorted,expected', [([2,3,3,2,4,5,1],[1,2,2,3,3,4,5])])
    def test_selection_sorts_ascending(self,unsorted,expected):
        sorted = sort.selection(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]

class Tests_compareto:
    @pytest.mark.parametrize('num,compareto,expected',[(1,4,True),(9,3,False)])
    def test_compare_defaults_to_ascending(self,num,compareto,expected):
        assert sort._compareto(num,compareto,'asc') == expected

    @pytest.mark.parametrize('num,compareto,expected',[(2,13,True),(34,12,False),(55,55,False)])
    def test_compare_ascending(self,num,compareto,expected):
        assert sort._compareto(num,compareto,'asc') == expected

    @pytest.mark.parametrize('num,compareto,expected',[(0,22,False),(19,-4,True),(22,22,False)])
    def test_compare_descending(self,num,compareto,expected):
        assert sort._compareto(num,compareto,'dsc') == expected