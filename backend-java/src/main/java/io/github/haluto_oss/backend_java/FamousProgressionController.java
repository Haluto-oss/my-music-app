package io.github.haluto_oss.backend_java;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/progressions")
public class FamousProgressionController {

    @Autowired
    private FamousProgressionService famousProgressionService;

    @CrossOrigin(origins = {"http://localhost:5173", "http://localhost:5174"})
    @GetMapping
    public List<FamousProgression> getFamousProgressions() {
        return famousProgressionService.getAllProgressions();
    }
}
