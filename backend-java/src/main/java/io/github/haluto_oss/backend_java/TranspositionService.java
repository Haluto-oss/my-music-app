// ファイル名: TranspositionService.java

package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import java.util.Collections;
import java.util.List;
import java.util.Map;

@Service
public class TranspositionService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${python.api.base.url:http://localhost:8000}")
    private String pythonApiBaseUrl;

    @SuppressWarnings("unchecked")
    // TranspositionService.java の transpose メソッドをこれに置き換えてください

    public List<String> transpose(String keyName, List<String> degrees) {
    // UriComponentsBuilderを使って、複数のdegreesパラメータを持つURLを組み立てる
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl(pythonApiBaseUrl)
                .path("/ai/transpose")
                .queryParam("key_name", keyName);

    // degreesリストの各要素を、それぞれ "degrees=..." というパラメータとして追加
        for (String degree : degrees) {
            builder.queryParam("degrees", degree);
        }
        String url = builder.toUriString();
        System.out.println("★ Calling Python Transpose API with URL: " + url);

        try {
        // シンプルなGETリクエストを実行
            ResponseEntity<Map<String, List<String>>> responseEntity = restTemplate.exchange(
                url,
                HttpMethod.GET,
                null, // GETリクエストなのでボディは無し
                new ParameterizedTypeReference<Map<String, List<String>>>() {}
            );
        
            Map<String, List<String>> response = responseEntity.getBody();
        
            if (response == null || !response.containsKey("transposed_chords")) {
                return null;
            }
        
            return response.get("transposed_chords");

        } catch (Exception e) {
            System.out.println("!!! Error calling Python Transpose API: " + e.getMessage());
            return null;
        }
    }
}