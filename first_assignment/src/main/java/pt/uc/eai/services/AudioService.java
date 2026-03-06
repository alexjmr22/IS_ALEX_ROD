package pt.uc.eai.services;

import pt.uc.eai.model.Payload;
import pt.uc.eai.model.Chunk;
import pt.uc.eai.model.Frame;
import pt.uc.eai.model.ServiceMetrics;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.IOException;
import java.util.List;

/**
 * Read-only audio processor for benchmarking.
 *
 * Deserializes the payload to measure deserialization cost,
 * processes the audio samples (read-only), and returns the
 * original packet unchanged — no re-serialization is performed.
 */
public class AudioService {
    private final ObjectMapper mapper;
    private ServiceMetrics metrics;

    public AudioService(ObjectMapper mapper) {
        this.mapper = mapper;
    }

    /**
     * Processes the incoming packet as a read-only audio consumer.
     *
     * @param packet the raw serialized payload (JSON or BSON bytes)
     * @return the original packet, unchanged
     * @throws IOException if deserialization fails
     */
    public byte[] process(byte[] packet) throws IOException {
        // --- Memory baseline (no System.gc() — it adds unpredictable pauses) ---
        final Runtime runtime = Runtime.getRuntime();
        final long startMem = runtime.totalMemory() - runtime.freeMemory();
        final long startTime = System.nanoTime();

        // --- 1. Deserialization (measured) ---
        final long startDe = System.nanoTime();
        final Payload payload = mapper.readValue(packet, Payload.class);
        final long endDe = System.nanoTime();

        // --- 2. Audio processing (read-only) ---
        processAudioSamples(payload);

        // --- 3. No serialization — payload was not modified ---
        // serializationTimeMs is reported as 0
        final long serializationTimeNs = 0;

        // --- Timing & memory snapshot ---
        final long endTime = System.nanoTime();
        final long endMem = runtime.totalMemory() - runtime.freeMemory();

        long memUsed = endMem - startMem;
        if (memUsed <= 0) {
            // Fallback: use incoming packet size when GC makes the delta negative
            memUsed = packet.length;
        }

        this.metrics = new ServiceMetrics(
                "AudioService",
                (endDe - startDe) / 1_000_000, // deserialization ms
                serializationTimeNs / 1_000_000, // serialization ms (0)
                (endTime - startTime) / 1_000_000, // total processing ms
                packet.length, // message size = original packet
                memUsed // memory used
        );

        // Return original packet — no re-encoding
        return packet;
    }

    /**
     * Iterates over every audio sample in the payload.
     * Extracted into a method to keep process() concise and to allow
     * the JIT to inline or optimise this hot loop independently.
     */
    private void processAudioSamples(Payload payload) {
        for (Chunk chunk : payload.getChunks()) {
            for (Frame frame : chunk.getFrames()) {
                final List<Double> samples = frame.getAudioSamples();
                // index-based loop avoids Iterator allocation per frame
                for (int i = 0, n = samples.size(); i < n; i++) {
                    // consume the sample (e.g. accumulate, validate, etc.)
                    double sum = 0;
                    sum += samples.get(i);
                }
            }
        }
    }

    public ServiceMetrics getMetrics() {
        return metrics;
    }
}
