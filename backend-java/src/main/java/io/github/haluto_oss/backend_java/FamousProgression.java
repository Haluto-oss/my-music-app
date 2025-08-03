package io.github.haluto_oss.backend_java;

import java.util.List;

public record FamousProgression(
    String name,
    String description,
    String defaultKey, // "key"から"defaultKey"に名前を明確化
    List<String> degrees // "chords"から"degrees"に変更
) {}