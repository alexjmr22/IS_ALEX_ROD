package pt.uc.eai.generator;

import pt.uc.eai.model.Chunk;
import pt.uc.eai.model.Frame;
import pt.uc.eai.model.Payload;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class PayloadGenerator {

    private final Random random;

    public PayloadGenerator(long seed) {
        this.random = new Random(seed);
    }

    public Payload generate(
            String stream_id,
            int numChunks,
            int framesPerChunk,
            int audioLen,
            int pixelsLen,
            int metadataLen
    ) {
        long timestamp = System.currentTimeMillis();
        List<Chunk> chunks = new ArrayList<>(numChunks);

        for (int c = 1; c <= numChunks; c++) {
            List<Frame> frames = new ArrayList<>(framesPerChunk);

            for (int f = 0; f < framesPerChunk; f++) {
                List<Double> audio = randomDoubles(audioLen, -1.0, 1.0);
                List<Integer> pixels = randomInts(pixelsLen, 0, 255);
                List<Double> metadata = randomDoubles(metadataLen, 0.0, 1.0);

                frames.add(new Frame(String.valueOf(f + 1), audio, pixels, metadata));
            }

            chunks.add(new Chunk(String.valueOf(c), frames));
        }

        return new Payload(stream_id, timestamp, chunks);
    }

    private List<Double> randomDoubles(int n, double min, double max) {
        List<Double> list = new ArrayList<>(n);
        double range = max - min;
        for (int i = 0; i < n; i++) {
            list.add(min + random.nextDouble() * range);
        }
        return list;
    }

    private List<Integer> randomInts(int n, int min, int maxInclusive) {
        List<Integer> list = new ArrayList<>(n);
        int bound = (maxInclusive - min) + 1;
        for (int i = 0; i < n; i++) {
            list.add(min + random.nextInt(bound));
        }
        return list;
    }
}
