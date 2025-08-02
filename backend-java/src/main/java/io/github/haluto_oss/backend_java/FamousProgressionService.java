package io.github.haluto_oss.backend_java;

import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class FamousProgressionService {

    // アプリケーションが知っている有名コード進行のリスト（設計図）
    private final List<FamousProgression> famousProgressions = List.of(
        new FamousProgression("カノン進行", "J-POPやクラシックで非常に人気の高いコード進行。", "C", List.of("I", "V", "vi", "iii", "IV", "I", "IV", "V")),
        new FamousProgression("王道進行", "J-POPのヒット曲で多用される、感動的な響きを持つ進行。", "C", List.of("IV", "V", "iii", "vi")),
        new FamousProgression("小室進行", "90年代のダンスミュージックを象徴する、切なくもダンサブルな進行。", "Am", List.of("vi", "IV", "V", "I")),
        new FamousProgression("丸の内進行", "椎名林檎さんの楽曲で有名になった、おしゃれで都会的な進行。", "G#m", List.of("iv", "VII", "III", "VI"))
    );

    /**
     * すべての有名コード進行のリスト（設計図）を返す
     */
    public List<FamousProgression> getAllProgressions() {
        return famousProgressions;
    }
}