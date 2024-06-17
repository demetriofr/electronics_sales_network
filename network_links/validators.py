from rest_framework.validators import ValidationError


class LevelNoMoreOrEqualThanTwoValidator:
    """Validator to check if a level is not more or equal than 2."""
    def __call__(self, attrs):

        previous_network_link = attrs.get('previous_network_link')  # Get previous network link

        level = self.calculate_level(previous_network_link)  # Calculate level

        if level > 2:
            raise ValidationError("The level should not be more than 2.")

    def calculate_level(self, previous_network_link, level=0):
        """Recursive function to calculate depth of nested network links."""

        # base case: if depth is greater than 2 or there is no previous network link, stop recursion
        if level > 2 or previous_network_link is None:
            return level

        # Recursively call the function for the previous link in the network
        return self.calculate_level(previous_network_link.previous_network_link, level + 1)
