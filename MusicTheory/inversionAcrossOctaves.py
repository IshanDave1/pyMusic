def calculate_evenness(points, range_start, range_end):
    # Sort the points in ascending order
    sorted_points = sorted(points)

    # Calculate the total number of points
    num_points = len(sorted_points)

    # Calculate the total range span
    range_span = range_end - range_start

    # Calculate the expected spacing between points in a perfectly even distribution
    expected_spacing = range_span / (num_points - 1)

    # Calculate the actual spacing between points
    actual_spacing = [sorted_points[i + 1] - sorted_points[i] for i in range(num_points - 1)]

    # Calculate the average spacing
    average_spacing = sum(actual_spacing) / len(actual_spacing)

    # Calculate the evenness score (ratio of actual spacing to expected spacing)
    evenness_score = average_spacing / expected_spacing

    return evenness_score


# Example usage:
points1 = [1, 3, 5, 7, 9]
points2 = [1, 2, 5, 8, 9]

range_start = 0
range_end = 10

evenness_score1 = calculate_evenness(points1, range_start, range_end)
evenness_score2 = calculate_evenness(points2, range_start, range_end)

print(f"Evenness score for points1: {evenness_score1}")
print(f"Evenness score for points2: {evenness_score2}")
