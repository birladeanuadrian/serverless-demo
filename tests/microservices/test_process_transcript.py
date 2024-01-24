import unittest

from app.microservices.process_transcript import chunk_is_safe, make_chunk_safe, segment_transcript


class MyTestCase(unittest.TestCase):
    def test_chunk_is_safe(self):
        chunks = ["A" * 8, "B" * 8]
        self.assertEqual(chunk_is_safe(chunks), True)

    def test_chunk_is_not_safe(self):
        chunks = ["A" * 20_000, "B" * 20_000]
        self.assertEqual(chunk_is_safe(chunks), False)

    def test_make_chunk_safe_no_change(self):
        lines = ["A" * 12, "B" * 12, "C" * 12]
        end, processed_chunks = make_chunk_safe(0, 3, lines)
        self.assertEqual(end, 3)
        self.assertEqual(processed_chunks, lines)

    def test_make_chunk_safe_remove_last_line(self):
        lines = ["A" * 12, "B" * 12, "C" * 12, "D" * 12_000, "E" * 12_000, "F" * 12_000]
        end, processed_chunks = make_chunk_safe(3, 6, lines)
        self.assertEqual(end, 5)
        self.assertEqual(processed_chunks, ["D" * 12_000, "E" * 12_000])

    def test_make_chunk_safe_remove_last_2_lines(self):
        lines = ["A" * 12, "B" * 12, "C" * 12, "D" * 20_000, "E" * 20_000, "F" * 20_000]
        end, processed_chunks = make_chunk_safe(3, 6, lines)
        self.assertEqual(end, 4)
        self.assertEqual(
            processed_chunks,
            [
                "D" * 20_000,
            ],
        )

    def test_segment_transcript_one_go(self):
        transcript = "\n".join(["A" * 10_000, "B" * 10_000])

        segmented_transcripts = list(segment_transcript(transcript))
        self.assertEqual([transcript], segmented_transcripts)

    def test_segment_transcript_even_lines(self):
        transcript = "\n".join(
            ["A" * 8_000, "B" * 8_000, "C" * 8_000, "D" * 8_000, "E" * 8_000, "F" * 8_000]
        )
        segmented_transcripts = list(segment_transcript(transcript))
        self.assertEqual(len(segmented_transcripts), 3)
        self.assertEqual(
            segmented_transcripts[0], "\n".join(["A" * 8_000, "B" * 8_000, "C" * 8_000])
        )
        self.assertEqual(
            segmented_transcripts[1],
            "\n".join(
                [
                    "C" * 8_000,
                    "D" * 8_000,
                    "E" * 8_000,
                ]
            ),
        )
        self.assertEqual(segmented_transcripts[2], "\n".join(["E" * 8_000, "F" * 8_000]))

    def test_segment_transcript_odd_lines(self):
        transcript = "\n".join(
            [
                "A" * 8_000,
                "B" * 8_000,
                "C" * 8_000,
                "D" * 8_000,
                "E" * 8_000,
            ]
        )
        segmented_transcripts = list(segment_transcript(transcript))
        self.assertEqual(len(segmented_transcripts), 2)
        self.assertEqual(
            segmented_transcripts[0], "\n".join(["A" * 8_000, "B" * 8_000, "C" * 8_000])
        )
        self.assertEqual(
            segmented_transcripts[1],
            "\n".join(
                [
                    "C" * 8_000,
                    "D" * 8_000,
                    "E" * 8_000,
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
