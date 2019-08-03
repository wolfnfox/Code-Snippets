import pytest

from sorting import sort

class Test_insert:
    @pytest.mark.parametrize('unsorted,expected', [([3,2,1],[1,2,3])])
    def test_insert_sorts_ascending(self,unsorted,expected):
        sorted = sort.insertion(unsorted)
        for i in range(0,len(expected)):
            assert sorted[i] == expected[i]