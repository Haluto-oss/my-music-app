package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

// フロントに返すための、新しいデータ構造を定義
record FamousProgressionResponse(
    String name,
    String description,
    String key,
    List<String> degrees,
    List<String> chords
) {}

@RestController
@RequestMapping("/api/progressions")
public class FamousProgressionController {

    @Autowired
    private FamousProgressionService famousProgressionService;

    @Autowired
    private TranspositionService transpositionService;

    @CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
    @GetMapping
    public List<FamousProgressionResponse> getFamousProgressions() {
        // すべてのコード進行の「設計図」を取得
        List<FamousProgression> progressions = famousProgressionService.getAllProgressions();

        // 各「設計図」を、デフォルトのキーでコードネームに変換して、フロントエンド用の形式にまとめる
        return progressions.stream().map(prog -> {
            // 移調サービスを使って、ディグリーをデフォルトキーのコードネームに変換
            List<String> transposedChords = transpositionService.transpose(prog.defaultKey(), prog.degrees());
            // フロントエンドに返すための新しいオブジェクトを作成
            return new FamousProgressionResponse(prog.name(), prog.description(), prog.defaultKey(), prog.degrees(), transposedChords);
        }).collect(Collectors.toList());
    }
}
