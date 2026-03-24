package pt.uc.eai;

import com.fasterxml.jackson.databind.ObjectMapper;

import de.undercouch.bson4jackson.BsonFactory;

public class Forma {
    
    public enum SerializationFormat {
        JSON, BSON
    }
    
    public static ObjectMapper createMapper(SerializationFormat format) {
        switch (format) {
            case JSON:
                return new ObjectMapper(); // ObjectMapper padrão para JSON
            case BSON:
                return new ObjectMapper(new BsonFactory()); // ObjectMapper com BsonFactory
            default:
                throw new IllegalArgumentException("Formato não suportado: " + format);
        }
    }
    
    public static SerializationFormat getFormatFromConfig() {
        String formatStr = Config.getProperty("serialization.format", "JSON").toUpperCase();
        try {
            return SerializationFormat.valueOf(formatStr);
        } catch (IllegalArgumentException e) {
            System.err.println("Formato inválido: " + formatStr + ". Usando JSON como padrão.");
            return SerializationFormat.JSON;
        }
    }
}