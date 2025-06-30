package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;

import java.util.Map;

@RestController
@RequestMapping("/api/chords")
public class ChordController {

    @Autowired
    private ChordService chordService;

    @CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
    @GetMapping
    public ResponseEntity<?> getChordAnalysis(@RequestParam String name) {
        System.out.println("★ Java Controller received with query: " + name);
        try {
            // ChordServiceに実際の処理を依頼する
            Map<String, Object> result = chordService.analyzeChord(name);

            // 成功した場合、キャッシュ無効化ヘッダーを付けて結果を返す
            return ResponseEntity.ok()
                    .header(HttpHeaders.CACHE_CONTROL, "no-cache, no-store, must-revalidate")
                    .header(HttpHeaders.PRAGMA, "no-cache")
                    .header(HttpHeaders.EXPIRES, "0")
                    .body(result);

        } catch (HttpClientErrorException e) {
            // Pythonサーバーからエラーが返ってきた場合、そのエラーをそのままフロントエンドに返す
            return ResponseEntity.status(e.getStatusCode()).body(e.getResponseBodyAsString());
        }
    }
}