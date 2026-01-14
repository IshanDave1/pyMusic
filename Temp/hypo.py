import hypothesis
from hypothesis import given
import hypothesis.strategies as st




# Define a strategy for generating lists of integers
@st.composite
def integer_lists(draw):
    # Generate a list of integers
    elements = draw(st.lists(st.integers()))
    return elements


# Define the property-based test
@given(integer_lists())
def test_sort_custom(input_list):
    # Copy the input list
    sorted_list = sorted(input_list.copy())

    # Check if the sorted list is indeed sorted
    assert input_list == sorted(input_list)


# Run the test
if __name__ == "__main__":
    test_sort_custom()
