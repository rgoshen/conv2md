"""Metrics and observability for markdown generation."""

import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


class ConversionStatus(Enum):
    """Status of markdown conversion."""

    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


@dataclass
class ConversionMetrics:
    """Metrics collected during markdown conversion."""

    # Timing metrics
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_seconds: Optional[float] = None

    # Content metrics
    message_count: int = 0
    total_content_size: int = 0
    output_size: int = 0

    # Processing metrics
    code_blocks_processed: int = 0
    images_processed: int = 0
    text_messages_processed: int = 0

    # Error metrics
    errors_encountered: int = 0
    warnings_issued: int = 0
    status: ConversionStatus = ConversionStatus.SUCCESS

    # Performance metrics
    processing_rate_chars_per_sec: Optional[float] = None
    memory_peak_mb: Optional[float] = None

    def finish(self) -> None:
        """Mark the conversion as finished and calculate final metrics."""
        self.end_time = time.time()
        self.duration_seconds = self.end_time - self.start_time

        if self.duration_seconds > 0 and self.total_content_size > 0:
            self.processing_rate_chars_per_sec = (
                self.total_content_size / self.duration_seconds
            )

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for logging/export."""
        return {
            "duration_seconds": self.duration_seconds,
            "message_count": self.message_count,
            "total_content_size": self.total_content_size,
            "output_size": self.output_size,
            "code_blocks_processed": self.code_blocks_processed,
            "images_processed": self.images_processed,
            "text_messages_processed": self.text_messages_processed,
            "errors_encountered": self.errors_encountered,
            "warnings_issued": self.warnings_issued,
            "status": self.status.value,
            "processing_rate_chars_per_sec": self.processing_rate_chars_per_sec,
            "memory_peak_mb": self.memory_peak_mb,
        }


class MetricsCollector:
    """Collects and reports metrics during markdown generation."""

    def __init__(self):
        """Initialize metrics collector."""
        self.logger = logging.getLogger(f"{__name__}.MetricsCollector")
        self.current_metrics: Optional[ConversionMetrics] = None

    def start_conversion(self) -> ConversionMetrics:
        """Start tracking a new conversion."""
        self.current_metrics = ConversionMetrics()
        self.logger.debug("Started conversion metrics collection")
        return self.current_metrics

    def record_message_processed(self, content_type: str, content_size: int) -> None:
        """Record that a message was processed."""
        if not self.current_metrics:
            return

        self.current_metrics.message_count += 1
        self.current_metrics.total_content_size += content_size

        if content_type == "code":
            self.current_metrics.code_blocks_processed += 1
        elif content_type == "image":
            self.current_metrics.images_processed += 1
        else:
            self.current_metrics.text_messages_processed += 1

    def record_error(self, error: Exception) -> None:
        """Record an error during conversion."""
        if not self.current_metrics:
            return

        self.current_metrics.errors_encountered += 1
        self.current_metrics.status = ConversionStatus.ERROR
        self.logger.error(f"Conversion error recorded: {error}")

    def record_warning(self, message: str) -> None:
        """Record a warning during conversion."""
        if not self.current_metrics:
            return

        self.current_metrics.warnings_issued += 1
        if self.current_metrics.status == ConversionStatus.SUCCESS:
            self.current_metrics.status = ConversionStatus.PARTIAL
        self.logger.warning(f"Conversion warning: {message}")

    def finish_conversion(self, output_size: int) -> ConversionMetrics:
        """Finish tracking conversion and return final metrics."""
        if not self.current_metrics:
            raise ValueError("No conversion in progress")

        self.current_metrics.output_size = output_size
        self.current_metrics.finish()

        # Log final metrics
        metrics_dict = self.current_metrics.to_dict()
        self.logger.info(f"Conversion completed: {metrics_dict}")

        return self.current_metrics
