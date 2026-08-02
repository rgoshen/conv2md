"""Unit tests for conversion metrics collection."""

import dataclasses
import time
import unittest
from unittest.mock import patch

from conv2md.markdown.metrics import (
    ConversionMetrics,
    ConversionStatus,
    MetricsCollector,
)


def _start_time_field():
    """Return the dataclass field descriptor for start_time."""
    fields = {f.name: f for f in dataclasses.fields(ConversionMetrics)}
    return fields["start_time"]


class TestConversionMetricsClock(unittest.TestCase):
    """Timing must come from the monotonic clock, not the wall clock."""

    def test_start_time_defaults_to_monotonic_clock(self):
        """start_time is seeded by time.monotonic, never by time.time."""
        default_factory = _start_time_field().default_factory

        self.assertIs(default_factory, time.monotonic)
        self.assertIsNot(default_factory, time.time)

    def test_finish_uses_monotonic_clock(self):
        """Given a finished conversion, end_time reads time.monotonic()."""
        metrics = ConversionMetrics(start_time=0.0)

        with patch("conv2md.markdown.metrics.time.monotonic", return_value=2000.0):
            metrics.finish()

        self.assertEqual(metrics.end_time, 2000.0)

    def test_duration_survives_backwards_wall_clock_step(self):
        """A wall-clock jump backwards must not corrupt duration or rate."""
        metrics = ConversionMetrics(start_time=500.0)
        metrics.total_content_size = 100

        # time.time() moving backwards (NTP step / DST) is irrelevant because
        # neither endpoint is read from the wall clock.
        with patch("conv2md.markdown.metrics.time.monotonic", return_value=502.5):
            with patch("conv2md.markdown.metrics.time.time", return_value=0.0):
                metrics.finish()

        self.assertEqual(metrics.duration_seconds, 2.5)
        self.assertEqual(metrics.processing_rate_chars_per_sec, 40.0)

    def test_real_clock_produces_non_negative_duration(self):
        """Given/When/Then: real timings stay ordered and non-negative."""
        metrics = ConversionMetrics()
        metrics.finish()

        self.assertIsNotNone(metrics.end_time)
        self.assertGreaterEqual(metrics.end_time, metrics.start_time)
        self.assertGreaterEqual(metrics.duration_seconds, 0.0)


class TestConversionMetricsCalculation(unittest.TestCase):
    """Duration and rate calculation behaviour must be preserved."""

    def test_processing_rate_guard_conditions(self):
        """Rate is only computed for a positive duration and content size."""
        cases = [
            ("no duration, no content", 0.0, 0, None),
            ("no duration, with content", 0.0, 100, None),
            ("with duration, no content", 2.0, 0, None),
            ("with duration and content", 2.0, 100, 50.0),
        ]

        for label, duration, content_size, expected_rate in cases:
            with self.subTest(case=label):
                metrics = ConversionMetrics(start_time=10.0)
                metrics.total_content_size = content_size

                with patch(
                    "conv2md.markdown.metrics.time.monotonic",
                    return_value=10.0 + duration,
                ):
                    metrics.finish()

                self.assertEqual(metrics.duration_seconds, duration)
                self.assertEqual(metrics.processing_rate_chars_per_sec, expected_rate)


class TestConversionMetricsSerialization(unittest.TestCase):
    """to_dict() must expose only measured fields."""

    def test_to_dict_keys(self):
        """The exported payload has an exact, stable key set."""
        metrics = ConversionMetrics()
        metrics.finish()

        self.assertEqual(
            set(metrics.to_dict()),
            {
                "duration_seconds",
                "message_count",
                "total_content_size",
                "output_size",
                "code_blocks_processed",
                "images_processed",
                "text_messages_processed",
                "errors_encountered",
                "warnings_issued",
                "status",
                "processing_rate_chars_per_sec",
            },
        )

    def test_to_dict_omits_unmeasured_memory_field(self):
        """memory_peak_mb is not reported because it is never measured."""
        metrics = ConversionMetrics()

        self.assertNotIn("memory_peak_mb", metrics.to_dict())
        self.assertFalse(hasattr(metrics, "memory_peak_mb"))


class TestMetricsCollectorLogging(unittest.TestCase):
    """finish_conversion finalizes metrics without reporting them."""

    def test_finish_conversion_does_not_log_metrics(self):
        """The caller logs the returned metrics, so this must stay silent."""
        collector = MetricsCollector()
        collector.start_conversion()

        with self.assertLogs(collector.logger, level="DEBUG") as captured:
            # Emit one record so assertLogs has something to assert against.
            collector.logger.debug("probe")
            collector.finish_conversion(output_size=42)

        self.assertEqual(
            [record.getMessage() for record in captured.records], ["probe"]
        )

    def test_finish_conversion_finalizes_and_returns_metrics(self):
        """Output size, duration, and status are set on the returned object."""
        collector = MetricsCollector()
        started = collector.start_conversion()
        collector.record_message_processed("text", 10)

        finished = collector.finish_conversion(output_size=42)

        self.assertIs(finished, started)
        self.assertIs(finished, collector.current_metrics)
        self.assertEqual(finished.output_size, 42)
        self.assertIsNotNone(finished.duration_seconds)
        self.assertEqual(finished.status, ConversionStatus.SUCCESS)

    def test_finish_conversion_without_start_raises(self):
        """Finishing an unstarted conversion is a programming error."""
        collector = MetricsCollector()

        with self.assertRaises(ValueError):
            collector.finish_conversion(output_size=1)


if __name__ == "__main__":
    unittest.main()
