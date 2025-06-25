package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;

import java.util.Map;

@RestController
@RequestMapping("/api/scales")
public class ScaleController {

    @Autowired
    private ScaleService scaleService;

    @CrossOrigin(origins = "http://localhost:5173")
    @GetMapping
    public ResponseEntity<?> getScaleAnalysis(@RequestParam String name) {
        System.out.println("★ Java ScaleController received with query: " + name);
        try {
            // ServiceからMap<String, Object>を受け取る
            Map<String, Object> result = scaleService.analyzeScale(name);

            // 成功した場合、ResponseEntityでラップして返す
            return ResponseEntity.ok()
                    .header(HttpHeaders.CACHE_CONTROL, "no-cache, no-store, must-revalidate")
                    .header(HttpHeaders.PRAGMA, "no-cache")
                    .header(HttpHeaders.EXPIRES, "0")
                    .body(result);

        } catch (HttpClientErrorException e) {
            // Pythonからの4xx系エラーを受け取った場合、その内容をそのまま返す
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }
}