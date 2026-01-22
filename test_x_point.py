import pytest
import numpy as np
from x_point import x_point, Shor, main


class TestXPoint:
    """Test cases for x_point function."""

    def test_x_point_basic(self):
        """Test basic x_point calculation."""
        By = np.array([1.5])
        Bz = np.array([2.0])
        theta = np.array([0.785398])

        result = x_point(By, Bz, theta)

        # Check that result is a numpy array
        assert isinstance(result, np.ndarray)
        # Check that result has expected shape
        assert len(result) == 1
        # Check that result is finite
        assert np.isfinite(result[0])

    def test_x_point_multiple_values(self):
        """Test x_point with multiple data points."""
        By = np.array([1.5, 2.0, 2.5])
        Bz = np.array([2.0, 1.5, 2.5])
        theta = np.array([0.785398, 0.523599, 0.698132])

        result = x_point(By, Bz, theta)

        # Check that result has correct length
        assert len(result) == 3
        # Check that all results are finite
        assert all(np.isfinite(result))

    def test_x_point_zero_bz(self):
        """Test x_point with Bz = 0."""
        By = np.array([1.5])
        Bz = np.array([0.0])
        theta = np.array([0.785398])

        result = x_point(By, Bz, theta)

        # Should still produce valid result due to +1 in denominator
        assert np.isfinite(result[0])

    def test_x_point_zero_by(self):
        """Test x_point with By = 0."""
        By = np.array([0.0])
        Bz = np.array([2.0])
        theta = np.array([0.785398])

        result = x_point(By, Bz, theta)

        # Result should be 0 or very close to 0
        assert abs(result[0]) < 1e-6


class TestShor:
    """Test cases for Shor function."""

    def test_shor_basic(self):
        """Test basic Shor function."""
        x = np.array([1.234567890])
        result = Shor(x)

        # Check rounding to 6 decimal places
        assert result[0] == pytest.approx(1.234568, abs=1e-6)

    def test_shor_array(self):
        """Test Shor with array input."""
        x = np.array([1.234567, 2.345678, 3.456789])
        result = Shor(x)

        # Check that result is rounded
        assert len(result) == 3
        assert all(np.isfinite(result))


class TestMain:
    """Test cases for main function."""

    def test_main_with_csv(self, tmp_path, monkeypatch):
        """Test main function with a valid CSV file."""
        # Create a temporary CSV file
        csv_content = "By,Bz,theta\n1.5,2.0,0.785398\n2.3,1.8,0.523599\n"
        csv_path = tmp_path / "solar_corona_magnetic_field.csv"
        csv_path.write_text(csv_content)

        # Change to temporary directory
        monkeypatch.chdir(tmp_path)

        # Run main function (should not raise exception)
        try:
            main()
        except SystemExit:
            pass  # main() might call sys.exit(), which is okay

    def test_main_missing_csv(self, tmp_path, monkeypatch, capsys):
        """Test main function with missing CSV file."""
        # Change to temporary directory where CSV doesn't exist
        monkeypatch.chdir(tmp_path)

        # Run main function
        main()

        # Check that error message is printed
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()

    def test_main_empty_csv(self, tmp_path, monkeypatch, capsys):
        """Test main function with empty CSV file."""
        # Create an empty CSV file
        csv_path = tmp_path / "solar_corona_magnetic_field.csv"
        csv_path.write_text("")

        # Change to temporary directory
        monkeypatch.chdir(tmp_path)

        # Run main function
        main()

        # Check that error message is printed
        captured = capsys.readouterr()
        assert "error" in captured.out.lower()

    def test_main_invalid_columns(self, tmp_path, monkeypatch, capsys):
        """Test main function with CSV missing required columns."""
        # Create a CSV file with wrong columns
        csv_content = "X,Y,Z\n1.5,2.0,0.785398\n"
        csv_path = tmp_path / "solar_corona_magnetic_field.csv"
        csv_path.write_text(csv_content)

        # Change to temporary directory
        monkeypatch.chdir(tmp_path)

        # Run main function
        main()

        # Check that error message is printed
        captured = capsys.readouterr()
        assert "error" in captured.out.lower()
