package pt.uc.eai.model;
import java.util.List;

public class Frame {
    private String frame_id;
    private List<Double> audio_samples;
    private List<Integer> pixels;
    private List<Double> metadata;

    public Frame() {}

    public Frame(String frame_id, List<Double> audio_samples, List<Integer> pixels, List<Double> metadata) {
        this.frame_id = frame_id;
        this.audio_samples = audio_samples;
        this.pixels = pixels;
        this.metadata = metadata;
    }

    public String getFrameId() {
        return frame_id;
    }

    public void setFrameId(String frame_id) {
        this.frame_id = frame_id;
    }

    public List<Double> getAudioSamples() {
        return audio_samples;
    }

    public void setAudioSamples(List<Double> audio_samples) {
        this.audio_samples = audio_samples;
    }

    public List<Integer> getPixels() {
        return pixels;
    }

    public void setPixels(List<Integer> pixels) {
        this.pixels = pixels;
    }

    public List<Double> getMetadata() {
        return metadata;
    }

    public void setMetadata(List<Double> metadata) {
        this.metadata = metadata;
    }
}
