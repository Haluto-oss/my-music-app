package io.github.haluto_oss.backend_java;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class FamousProgressionService {

    public List<FamousProgression> getAllProgressions() {
        // ここに有名コード進行のデータを作成します
        // 将来的には、このデータをデータベースやファイルから読み込むように拡張できます
        return List.of(
            new FamousProgression("カノン進行", "J-POPやクラシックで非常に人気の高いコード進行。", "C Major", List.of("C", "G", "Am", "Em", "F", "C", "F", "G")),
            new FamousProgression("王道進行", "J-POPのヒット曲で多用される、感動的な響きを持つ進行。", "C Major", List.of("F", "G", "Em", "Am")),
            new FamousProgression("小室進行", "90年代のダンスミュージックを象徴する、切なくもダンサブルな進行。", "A Minor", List.of("Am", "F", "G", "C")),
            new FamousProgression("丸の内進行", "椎名林檎さんの楽曲で有名になった、おしゃれで都会的な進行。", "G# Minor", List.of("G#m7", "C#7", "F#M7", "B7"))
        );
    }
}