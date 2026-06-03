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

        center_x = outer_radius + self.margin
        center_y = outer_radius + self.margin

        if center_x - outer_radius < self.margin:
            center_x = w // 2
        if center_y + outer_radius > h - self.margin:
            center_y = h // 2

        return center_x, center_y, outer_radius, inner_radius

    def hovered_chord(self, frame, point):
        if point is None:
            return None

        center_x, center_y, outer_radius, inner_radius = self._layout(frame)
        dx = point[0] - center_x
        dy = point[1] - center_y
        distance = math.hypot(dx, dy)

        if distance < inner_radius or distance > outer_radius:
            return None

        angle = math.degrees(math.atan2(dy, dx))
        if angle < 0:
            angle += 360

        chord_index = int(angle // 45) % len(self.chords)
        return self.chords[chord_index]

    def draw(self, frame, hover_point=None):
        center_x, center_y, outer_radius, inner_radius = self._layout(frame)
        hovered_chord = self.hovered_chord(frame, hover_point)
        overlay = frame.copy()

        for i, chord in enumerate(self.chords):
            start_angle = i * 45
            end_angle = start_angle + 45

            mid_angle = math.radians(start_angle + 22.5)
            is_hovered = chord == hovered_chord
            fill_color = (40, 120, 220) if is_hovered else (36, 36, 36)
            border_color = (255, 255, 255) if is_hovered else (180, 180, 180)
            text_color = (255, 255, 255)
            thickness = 4 if is_hovered else 2

            # Sector border
            cv2.ellipse(
                overlay,
                (center_x, center_y),
                (outer_radius, outer_radius),
                0,
                start_angle,
                end_angle,
                fill_color,
                -1
            )

            cv2.ellipse(
                overlay,
                (center_x, center_y),
                (outer_radius, outer_radius),
                0,
                start_angle,
                end_angle,
                border_color,
                thickness
            )

            boundary_angle = math.radians(start_angle)
            boundary_x = int(center_x + outer_radius * math.cos(boundary_angle))
            boundary_y = int(center_y + outer_radius * math.sin(boundary_angle))

            cv2.line(
                overlay,
                (center_x, center_y),
                (boundary_x, boundary_y),
                border_color,
                thickness
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
                text_color,
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

        if hovered_chord:
            cv2.putText(
                frame,
                hovered_chord,
                (center_x - 24, center_y + 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2
            )

        return hovered_chord
