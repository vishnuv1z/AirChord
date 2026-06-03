import cv2
import math


class ChordWheel:
    def __init__(self):
        self.chords = ["C", "G", "D", "A", "E", "Am", "Em", "Dm"]

        self.margin = 24

    def _layout(self, frame):
        h, w, _ = frame.shape

        outer_radius = max(70, min(150, int(min(w, h) * 0.28)))
        inner_radius = max(28, int(outer_radius * 0.38))

        center_x = w - outer_radius - self.margin
        center_y = outer_radius + self.margin

        if center_x - outer_radius < self.margin:
            center_x = w // 2
        if center_y + outer_radius > h - self.margin:
            center_y = h // 2

        return center_x, center_y, outer_radius, inner_radius

    def draw(self, frame):
        center_x, center_y, outer_radius, inner_radius = self._layout(frame)
        overlay = frame.copy()

        for i, chord in enumerate(self.chords):
            start_angle = i * 45
            end_angle = start_angle + 45

            mid_angle = math.radians(start_angle + 22.5)

            # Sector border
            cv2.ellipse(
                overlay,
                (center_x, center_y),
                (outer_radius, outer_radius),
                0,
                start_angle,
                end_angle,
                (36, 36, 36),
                -1
            )

            cv2.ellipse(
                overlay,
                (center_x, center_y),
                (outer_radius, outer_radius),
                0,
                start_angle,
                end_angle,
                (180, 180, 180),
                2
            )

            boundary_angle = math.radians(start_angle)
            boundary_x = int(center_x + outer_radius * math.cos(boundary_angle))
            boundary_y = int(center_y + outer_radius * math.sin(boundary_angle))

            cv2.line(
                overlay,
                (center_x, center_y),
                (boundary_x, boundary_y),
                (180, 180, 180),
                2
            )

            # Label position
            text_radius = (outer_radius + inner_radius) // 2

            text_x = int(
                center_x +
                text_radius * math.cos(mid_angle)
            )

            text_y = int(
                center_y +
                text_radius * math.sin(mid_angle)
            )

            cv2.putText(
                overlay,
                chord,
                (text_x - 15, text_y + 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                max(0.55, outer_radius / 190),
                (255, 255, 255),
                2
            )

        cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)

        # Outer ring
        cv2.circle(
            frame,
            (center_x, center_y),
            outer_radius,
            (210, 210, 210),
            3
        )

        # Inner ring
        cv2.circle(
            frame,
            (center_x, center_y),
            inner_radius,
            (210, 210, 210),
            3
        )

        cv2.circle(
            frame,
            (center_x, center_y),
            inner_radius - 2,
            (25, 25, 25),
            -1
        )
