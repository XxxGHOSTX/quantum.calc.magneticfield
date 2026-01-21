import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def Shor(x):
    """
    Simplified Shor's algorithm approximation.

    In reality, Shor's algorithm is for integer factorization in quantum computing.
    For this magnetic field calculation, we'll use a more appropriate rounding function.

    Args:
        x: The value to process.

    Returns:
        The processed value.
    """
    # Since Shor's algorithm doesn't apply here, we'll use proper rounding
    return np.round(x, decimals=6)


def x_point(By, Bz, theta):
    """
    Calculates the x-coordinate of the x-point in a magnetic field.

    Args:
        By: The By component of the magnetic field.
        Bz: The Bz component of the magnetic field.
        theta: The angle between the By and Bz components of the magnetic field.

    Returns:
        The x-coordinate of the x-point.
    """
    # Calculate the x-coordinate using standard magnetic field formulas
    # The x-point location in magnetic reconnection theory
    x = np.sqrt(By**2 / (Bz**2 + 1)) * np.cos(theta)

    # Apply rounding to improve numerical stability
    x = Shor(x)

    return x


def main():
    try:
        # Load the data on the magnetic field in the solar corona.
        data = pd.read_csv("solar_corona_magnetic_field.csv")

        # Check if the required columns are present in the DataFrame.
        required_columns = ["By", "Bz", "theta"]
        if not all(column in data.columns for column in required_columns):
            raise ValueError("The CSV file must contain columns 'By', 'Bz', and 'theta'.")

        # Get the values of By, Bz, and theta from the DataFrame and convert them to NumPy arrays.
        By = np.array(data["By"])
        Bz = np.array(data["Bz"])
        theta = np.array(data["theta"])

        # Calculate the x-coordinate of the x-point for each data point
        x_points = x_point(By, Bz, theta)

        # Print the results
        print("X-Point Calculation Results:")
        print("=" * 50)
        for i in range(len(x_points)):
            print(f"Data Point {i+1}: x-coordinate = {x_points[i]:.6f}")

        # Optional: Create a visualization
        plt.figure(figsize=(10, 6))
        plt.plot(x_points, marker='o', linestyle='-', linewidth=2, markersize=8)
        plt.xlabel('Data Point Index')
        plt.ylabel('X-coordinate')
        plt.title('X-Point Coordinates in Magnetic Field')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('x_point_results.png')
        print("\nVisualization saved as 'x_point_results.png'")

    except FileNotFoundError:
        print("Error: The CSV file 'solar_corona_magnetic_field.csv' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
    except pd.errors.ParserError:
        print("Error: The CSV file could not be parsed. Please check its format.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Run the code
    main()
