package pt.uc.eai.services;

import com.fasterxml.jackson.databind.ObjectMapper;
import pt.uc.eai.model.Payload;

import java.io.IOException;

public class Encoder {

    private final ObjectMapper mapper;

    public Encoder(ObjectMapper mapper) {
        this.mapper = mapper;
    }

    public byte[] encode(Payload payload) throws IOException {
        // Serializa o objeto Payload para byte[]
        return mapper.writeValueAsBytes(payload);
    }

    public Payload decode(byte[] data) throws IOException {
        // Desserializa byte[] para objeto Payload
        return mapper.readValue(data, Payload.class);
    }
}
