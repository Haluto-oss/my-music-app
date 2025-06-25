package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Map;

@Service
public class ScaleService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${python.api.base.url:http://localhost:8000}")
    private String pythonApiBaseUrl;

    public Map<String, Object> analyzeScale(String scaleName) {
        // PythonのAPIを呼び出すためのURLを、クエリパラメータ形式で安全に組み立てる
        String url = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
                .path("/ai/analyze/scale")
                .queryParam("name", scaleName)
                .toUriString();

        // ChordServiceと同様に、型情報を正確に指定してAPIを呼び出す
        ResponseEntity<Map<String, Object>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<Map<String, Object>>() {}
        );

        return response.getBody();
    }
}