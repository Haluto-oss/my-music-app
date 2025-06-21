package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.HttpClientErrorException;

import java.util.Map;

@RestController
@RequestMapping("/api/chords") // このコントローラーは /api/chords に関連するリクエストを処理する
public class ChordController {

    // ChordServiceを自動的に注入してもらう
    @Autowired
    private ChordService chordService;

    @CrossOrigin(origins = "http://localhost:5173") // フロントエンドからのアクセスを許可
    @GetMapping("/{chordName}") // 例: /api/chords/Cmaj7 にアクセスするとこれが呼ばれる
    public ResponseEntity<?> getChordAnalysis(@PathVariable String chordName) {

         // ↓デバッグを確認するためのコード
        System.out.println("★ Java Controller received: " + chordName);
        try {
            // ChordServiceに実際の処理を依頼する
            Map<String, Object> result = chordService.analyzeChord(chordName);
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