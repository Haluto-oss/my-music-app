package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder; // <--- このimport文を追加

import java.util.Map;

@Service
public class ChordService {

    @Autowired
    private RestTemplate restTemplate;

    private final String pythonApiBaseUrl = "http://localhost:8000";

    // ↓↓↓↓↓↓ このメソッドを丸ごと書き換えます ↓↓↓↓↓↓
    public Map<String, Object> analyzeChord(String chordName) {
        // UriComponentsBuilderを使って、URLエンコーディングの問題を安全に解決する
        String url = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
                .path("/ai/analyze/chord/{chordName}")
                .buildAndExpand(chordName)
                .toUriString();

        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        return response.getBody();
    }
}